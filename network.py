# coding=utf-8
# Copyright 2018 The Dopamine Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import collections

import gin
import tensorflow as tf
from dopamine.discrete_domains import atari_lib

from dopamine.discrete_domains.gym_lib import BasicDiscreteDomainNetwork


STREET_FIGHTER_V_MIN_VALS = -1.0
STREET_FIGHTER_V_MAX_VALS = 1.0


@gin.configurable
class StreetFighterVRainbowNetwork(tf.keras.Model):
  """Keras Rainbow network for Street Fighter V."""

  def __init__(self, num_actions, num_atoms, support, name=None):
    """Builds the deep network used to compute the agent's Q-values.

    It rescales the input features to a range that yields improved performance.

    Args:
      num_actions: int, number of actions.
      num_atoms: int, the number of buckets of the value function distribution.
      support: tf.linspace, the support of the Q-value distribution.
      name: str, used to create scope for network parameters.
    """
    super(StreetFighterVRainbowNetwork, self).__init__(name=name)
    self.net = BasicDiscreteDomainNetwork(
        STREET_FIGHTER_V_MIN_VALS, STREET_FIGHTER_V_MAX_VALS, num_actions, num_atoms=num_atoms)
    self.num_actions = num_actions
    self.num_atoms = num_atoms
    self.support = support

  def call(self, state):
    x = self.net(state)
    logits = tf.reshape(x, [-1, self.num_actions, self.num_atoms])
    probabilities = tf.keras.activations.softmax(logits)
    q_values = tf.reduce_sum(self.support * probabilities, axis=2)
    return atari_lib.RainbowNetworkType(q_values, logits, probabilities)
