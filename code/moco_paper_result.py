import os
import numpy as np
import matplotlib.pyplot as plt

from abc import ABC, abstractmethod

import utilities

class MocoPaperResult(ABC):
    def __init__(self):
        self.emg_sensor_names = [
            'SOL', 'GAS', 'TA', 'MH', 'BF', 'VL', 'VM', 'RF', 'GMAX', 'GMED']

    @abstractmethod
    def generate_results(self):
        pass

    @abstractmethod
    def report_results(self):
        pass

    def shift(self, time, y, initial_time=None, final_time=None, starting_time=None):
        if not initial_time:
            initial_time = self.initial_time
        if not final_time:
            final_time = self.final_time
        if not starting_time:
            starting_time = self.initial_time
        return utilities.shift_data_to_cycle(initial_time, final_time,
            starting_time, time, y, cut_off=True)

    def plot(self, ax, time, y, shift=True, fill=False, *args, **kwargs):
        if shift:
            shifted_time, shifted_y = self.shift(time, y)
        else:
            duration = self.final_time - self.initial_time
            shifted_time, shifted_y = self.shift(time, y,
                starting_time=self.initial_time + 0.5 * duration)

        duration = self.final_time - self.initial_time
        if fill:
            return ax.fill_between(
                100.0 * shifted_time / duration,
                shifted_y,
                np.zeros_like(shifted_y),
                *args,
                clip_on=False, **kwargs)
        else:
            return ax.plot(100.0 * shifted_time / duration, shifted_y, *args,
                           clip_on=False, **kwargs)

    def load_electromyography(self, root_dir):
        # anc = utilities.ANCFile(
        #     os.path.join(root_dir, 'resources/Rajagopal2016/emg_walk_raw.anc'))
        # raw = anc.data
        # fields_to_remove = []
        # for name in anc.names:
        #     if name != 'time' and name not in self.emg_sensor_names:
        #         fields_to_remove.append(name)
        # del name
        #
        # # We don't actually use the data that is initially in this object. We
        # # will overwrite all the data with the filtered data.
        # filtered_emg = utilities.remove_fields_from_structured_ndarray(raw,
        #     fields_to_remove).copy()
        #
        # # Debugging.
        # emg_fields = list(filtered_emg.dtype.names)
        # emg_fields.remove('time')
        # for expected_field in self.emg_sensor_names:
        #     if expected_field not in emg_fields:
        #         raise Exception("EMG field {} not found.".format(
        #             expected_field))
        #
        # # Filter all columns.
        # for name in filtered_emg.dtype.names:
        #     if name != 'time':
        #         scaled_raw = anc.ranges[name] * 2 / 65536.0 * 0.001 * anc[name]
        #         filtered_emg[name] = utilities.filter_emg(
        #             scaled_raw.copy(), anc.rates[name])
        #         filtered_emg[name] /= np.max(filtered_emg[name])
        # return filtered_emg
        return np.genfromtxt(os.path.join(root_dir, 'resources',
                                         'PerryBurnfieldElectromyography.csv'),
                            names=True,
                            delimiter=',')
