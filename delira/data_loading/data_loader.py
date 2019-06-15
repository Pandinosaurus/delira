import numpy as np
from batchgenerators.dataloading.data_loader import SlimDataLoaderBase
from multiprocessing import Queue
from queue import Empty

from .dataset import AbstractDataset


class BaseDataLoader(SlimDataLoaderBase):
    """
    Class to create a data batch out of data samples

    """

    def __init__(self, dataset: AbstractDataset,
                 sampler_queue: Queue,
                 batch_size=1, num_batches=None, seed=1):
        """

        Parameters
        ----------
        dataset : AbstractDataset
            dataset to perform sample loading
        batch_size : int
            number of samples per batch
        sampler_queue : :class:`multiprocessing.Queue`
            the queue, the sample indices to load will be put to.
            Necessary for interprocess communication
        num_batches : int
            number of batches to load
        seed : int
            seed for Random Number Generator

        Raises
        ------
        AssertionError
            `sampler` is not :obj:`None` and `sampler` is not an instance of
            the :class:`.sampler.AbstractSampler`

        See Also
        --------
        :class:`.sampler.SequentialSampler`

        """

        # store dataset in self._data
        super().__init__(dataset, batch_size)

        self.sampler_queue = sampler_queue

        self.n_samples = len(dataset)
        if num_batches is None:
            num_batches = len(dataset) // batch_size

        self.num_batches = num_batches
        self._seed = seed
        np.random.seed(seed)

        self._batches_generated = 0

    def generate_train_batch(self):
        """
        Generate Indices which behavior based on self.sampling gets data based
        on indices

        Returns
        -------
        dict
            data and labels

        Raises
        ------
        StopIteration
            If the maximum number of batches has been generated
        """

        if self._batches_generated >= self.num_batches:
            raise StopIteration
        else:
            self._batches_generated += 1
            idxs = None
            while idxs is None:
                try:
                    idxs = self.sampler_queue.get(timeout=0.2)
                except Empty:
                    pass

            # idxs = self.sampler_queue.get()

            result = [self._get_sample(_idx) for _idx in idxs]

            result_dict = {}

            # concatenate dict entities by keys
            for _result_dict in result:
                for key, val in _result_dict.items():
                    if key in result_dict.keys():
                        result_dict[key].append(val)
                    else:
                        result_dict[key] = [val]

            # convert list to numpy arrays
            for key, val_list in result_dict.items():
                result_dict[key] = np.asarray(val_list)

            return result_dict

    def _get_sample(self, index):
        """
        Helper functions which returns an element of the dataset

        Parameters
        ----------
        index : int
            index specifying which sample to return

        Returns
        -------
        dict
            Returned Data
        """
        return self._data[index]
