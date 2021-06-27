import gin
import tensorflow as tf

gin.constant('street_fighter_v.OBSERVATION_SHAPE', (87, 1))
gin.constant('street_fighter_v.OBSERVATION_DTYPE', tf.float32)
gin.constant('street_fighter_v.STACK_SIZE', 1)
