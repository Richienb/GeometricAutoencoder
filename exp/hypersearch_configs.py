def MNIST():
    overrides = {'dataset__name': 'MNIST'}


def FashionMNIST():
    overrides = {'dataset__name': 'FashionMNIST'}


def Spheres():
    overrides = {'dataset__name': 'Spheres'}


def CIFAR():
    overrides = {'dataset__name': 'CIFAR'}


def Zilionis():
    overrides = {'dataset__name': 'Zilionis'}


def PBMC():
    overrides = {'dataset__name': 'PBMC'}


def Images():
    overrides = {'dataset__name': 'Images'}


def CElegans():
    overrides = {'dataset__name': 'CElegans'}


def Earth():
    overrides = {'dataset__name': 'Earth'}


def add_datasets(experiment):
    experiment.named_config(MNIST)
    experiment.named_config(FashionMNIST)
    experiment.named_config(Spheres)
    experiment.named_config(CIFAR)
    experiment.named_config(Zilionis)
    experiment.named_config(PBMC)
    experiment.named_config(CElegans)
    experiment.named_config(Images)
    experiment.named_config(Earth)


def Vanilla():
    train_module = 'train_model'
    hyperparameter_space = {
        'batch_size': ('Integer', 16, 128)
    }
    overrides = {'model__name': 'VanillaAutoencoderModel'}


# our birected, topological loss term
def TopoRegEdgeSymmetric():
    train_module = 'train_model'
    hyperparameter_space = {
        'model__parameters__lam': ('Real', 0.01, 3, 'log-uniform'),
        'batch_size': ('Integer', 16, 128)
    }
    overrides = {
        'model__name': 'TopologicallyRegularizedAutoencoder',
        'model__parameters__toposig_kwargs__match_edges': 'symmetric',
    }


def GeomReg():
    train_module = 'train_model'
    hyperparameter_space = {
        'model__parameters__lam': ('Real', 0.001, 10, 'log-uniform'),
        'batch_size': ('Integer', 16, 128)
    }
    overrides = {
        'model__name': 'GeometricAutoencoder',
    }


# alternatives (from an early test phase)
def TopoReg():
    train_module = 'train_model'
    hyperparameter_space = {
        'model__parameters__lam': ('Real', 0.01, 1, 'log-uniform')
    }
    overrides = {
        'model__name': 'TopologicallyRegularizedAutoencoder',
    }


def TopoRegVertex():
    train_module = 'train_model'
    hyperparameter_space = {
        'model__parameters__lam': ('Real', 0.01, 1, 'log-uniform')
    }
    overrides = {
        'model__name': 'TopologicallyRegularizedAutoencoder',
        'model__parameters__toposig_kwargs__sort_selected': True,
    }


def add_models(experiment):
    experiment.named_config(Vanilla)
    experiment.named_config(TopoReg)
    experiment.named_config(TopoRegVertex)
    experiment.named_config(TopoRegEdgeSymmetric)
    experiment.named_config(GeomReg)


def PCA():
    train_module = 'fit_competitor'
    overrides = {
        'model__name': 'PCA',
        'model__parameters__n_components': 2
    }
    # There are no real parameters for PCA
    n_calls = 2
    n_random_starts = 1


def TSNE():
    train_module = 'fit_competitor'
    hyperparameter_space = {
        'model__parameters__perplexity': ('Real', 5., 50., 'uniform'),
        'model__parameters__learning_rate': ('Real', 10., 1000., 'log-uniform'),

    }
    overrides = {
        'model__name': 'TSNE',
        'model__parameters__n_components': 2,
        'model__parameters__n_iter': 1500
    }


def Isomap():
    train_module = 'fit_competitor'
    hyperparameter_space = {
        'model__parameters__n_neighbors': ('Integer', 15, 500),
    }
    overrides = {
        'model__name': 'Isomap',
        'model__parameters__n_components': 2,
        'model__parameters__n_jobs': 4
    }


def UMAP():
    train_module = 'fit_competitor'
    hyperparameter_space = {
        'model__parameters__n_neighbors': ('Integer', 15, 500),
        'model__parameters__min_dist': ('Real', 0.0, 1., 'uniform')
    }
    overrides = {
        'model__name': 'UMAP',
        'model__parameters__n_components': 2,
        'model__parameters__metric': 'euclidean'
    }


def ParametricUMAP():
    train_module = 'fit_competitor'
    hyperparameter_space = {
        'model__parameters__n_neighbors': ('Integer', 15, 500),
        'model__parameters__min_dist': ('Real', 0.0, 1., 'uniform')
    }
    overrides = {
        'model__name': 'ParametricUMAP',
        'model__parameters__n_components': 2,
        'model__parameters__autoencoder_loss': True,
        'model__parameters__parametric_reconstruction': True
    }


def add_competitors(experiment):
    experiment.named_config(PCA)
    experiment.named_config(TSNE)
    experiment.named_config(Isomap)
    experiment.named_config(UMAP)
    experiment.named_config(ParametricUMAP)