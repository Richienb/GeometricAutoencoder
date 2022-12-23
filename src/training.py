"""Training classes."""
import os

import torch
from src.evaluation.eval import Multi_Evaluation
from src.visualization import plot_losses
from torch.autograd import Variable
from torch.utils.data import DataLoader
from .datasets.splitting import split_dataset
import numpy as np

os.environ["GEOMSTATS_BACKEND"] = "pytorch"


class TrainingLoop():
    """Training a model using a dataset."""

    def __init__(self, model, dataset, n_epochs, batch_size, learning_rate,
                 weight_decay=1e-5, device='cuda', callbacks=None):
        """Training of a model using a dataset and the defined callbacks.

        Args:
            model: AutoencoderModel
            dataset: Dataset
            n_epochs: Number of epochs to train
            batch_size: Batch size
            learning_rate: Learning rate
            callbacks: List of callbacks
        """
        self.model = model
        self.dataset = dataset
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.device = device
        self.callbacks = callbacks if callbacks else []

        self.with_geom_loss = False

    def _execute_callbacks(self, hook, local_variables):
        stop = False
        for callback in self.callbacks:
            # Convert return value to bool --> if callback doesn't return
            # anything we interpret it as False
            stop |= bool(getattr(callback, hook)(**local_variables))
        return stop

    def on_epoch_begin(self, local_variables):
        """Call callbacks before an epoch begins."""
        return self._execute_callbacks('on_epoch_begin', local_variables)

    def on_epoch_end(self, local_variables):
        """Call callbacks after an epoch is finished."""
        return self._execute_callbacks('on_epoch_end', local_variables)

    def on_batch_begin(self, local_variables):
        """Call callbacks before a batch is being processed."""
        self._execute_callbacks('on_batch_begin', local_variables)

    def on_batch_end(self, local_variables):
        """Call callbacks after a batch has be processed."""
        self._execute_callbacks('on_batch_end', local_variables)

    # pylint: disable=W0641
    def __call__(self):
        """Execute the training loop."""
        model = self.model
        dataset = self.dataset
        n_epochs = self.n_epochs
        batch_size = self.batch_size
        learning_rate = self.learning_rate

        n_instances = len(dataset)
        # TODO: Currently we drop the last batch as it might not evenly divide
        # the dataset. This is necassary because the surrogate approach does
        # not yet support changes in the batch dimension.

        train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True,
                                  pin_memory=True, drop_last=True)
        n_batches = len(train_loader)

        optimizer = torch.optim.Adam(
            model.parameters(), lr=learning_rate,
            weight_decay=self.weight_decay)

        # initialize metric dictionary
        # metrics = {key: [] for key in self.evaluation["metrics"]}
        # stds = {key: [] for key in self.evaluation["metrics"]}

        epoch = 1
        for epoch in range(1, n_epochs + 1):
            if self.on_epoch_begin(remove_self(locals())):
                break

            geom_error = 0

            # data = None
            # latents = None

            for batch, (img, label) in enumerate(train_loader):

                if self.device == 'cuda':
                    img = img.cuda(non_blocking=True)

                self.on_batch_begin(remove_self(locals()))

                # Set model into training mode and compute loss
                model.train()
                loss, loss_components = self.model(img)

                # Optimize
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                if self.with_geom_loss:
                    geom_error += loss_components["loss.geom_error"]

                # if data is None:
                #    data = img
                #    latents = model.autoencoder.latent_activations.detach().clone()
                # else:
                #    data = torch.cat((data, img))
                #    latents = torch.cat((latents, model.autoencoder.latent_activations.detach().clone()))

                # Call callbacks
                self.on_batch_end(remove_self(locals()))

            if self.on_epoch_end(remove_self(locals())):
                break

            """
            else:
                # TODO: this could create problems, no? The detaching. Or is it not inplace?!
                # TODO: do I really need to create a deepcopy here? PROBABLY NOT! But what about

                # TODO: move to epoch end callback

                if self.evaluation and "metrics" in self.evaluation:
                    k_min, k_max, k_step = \
                        self.evaluation['k_min'], self.evaluation['k_max'], self.evaluation['k_step']
                    ks = list(range(k_min, k_max + k_step, k_step))

                    print("BEGIN")
                    evaluator = Multi_Evaluation(
                        dataloader=train_loader, seed=self._seed, model=model)

                    # labels = dataset.targets
                    # data = dataset.data.to(self.device)
                    # print(data.shape)
                    # print("\nhere\n")
                    # model.autoencoder(dataset)
                    # print("\nendhere\n")

                    # latents = model.latent_activations.to(self.device)
                    data = data.view(latents.shape[0], -1)

                    nth = 500

                    # reduce size of dataset
                    data = data[nth::]
                    latents = latents[nth::]

                    # TODO: remove cpu(), do everything on GPU. So implement the metrics in torch
                    epoch_measures = evaluator.calc_metrics(self.evaluation["metrics"], data, latents, ks)

                    for key in self.evaluation["metrics"]:
                        metrics[key].append(epoch_measures[key])
                        stds[key].append(0)

                    print(epoch_measures)
                    print(metrics)

        plot_losses(
            metrics,
            stds,
            save_file=os.path.join(self.rundir, 'metrics_training.png')
        )

        """

        return epoch


def remove_self(dictionary):
    """Remove entry with name 'self' from dictionary.

    This is useful when passing a dictionary created with locals() as kwargs.

    Args:
        dictionary: Dictionary containing 'self' key

    Returns:
        dictionary without 'self' key

    """
    del dictionary['self']
    return dictionary
