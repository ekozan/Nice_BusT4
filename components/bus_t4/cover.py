import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import spi
from esphome.components import cover
from esphome.const import CONF_ID, CONF_MODE,CONF_ADDRESS, CONF_UPDATE_INTERVAL, CONF_USE_ADDRESS

DEPENDENCIES = ["spi","cover"]
CODEOWNERS = ["@ekozan"]

MULTI_CONF = True

bus_t4_ns = cg.esphome_ns.namespace('bus_t4')
Nice = bus_t4_ns.class_('NiceBusT4', cover.Cover, cg.Component)


bus_t4 = bus_t4_ns.class_("BusT4Component", cover.Cover, cg.Component, spi.SPIDevice)

Mode = spi.spi_ns.enum("SPIMode")
MODES = {
    "0": Mode.MODE0,
    "1": Mode.MODE1,
    "2": Mode.MODE2,
    "3": Mode.MODE3,
    "MODE0": Mode.MODE0,
    "MODE1": Mode.MODE1,
    "MODE2": Mode.MODE2,
    "MODE3": Mode.MODE3,
}

BitOrder = spi.spi_ns.enum("SPIBitOrder")
ORDERS = {
    "msb_first": BitOrder.BIT_ORDER_MSB_FIRST,
    "lsb_first": BitOrder.BIT_ORDER_LSB_FIRST,
}
CONF_BIT_ORDER = "bit_order"

CONFIG_SCHEMA = cover.COVER_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(Nice),
    cv.Optional(CONF_ADDRESS): cv.hex_uint16_t,
    cv.Optional(CONF_USE_ADDRESS): cv.hex_uint16_t,
    cv.Optional(CONF_UPDATE_INTERVAL): cv.positive_time_period_milliseconds,
}).extend(cv.COMPONENT_SCHEMA).extend(spi.spi_device_schema(False, "1MHz"))


async def to_code(config):
   var = cg.new_Pvariable(config[CONF_ID])
    if CONF_ADDRESS in config:
        cg.add(var.set_to_address(config[CONF_ADDRESS]))
    if CONF_USE_ADDRESS in config:
        cg.add(var.set_from_address(config[CONF_USE_ADDRESS]))
    if CONF_UPDATE_INTERVAL in config:
        cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL]))
        
    await cg.register_component(var, config)
    await cover.register_cover(var, config)
    cg.add(var.set_mode(config[CONF_MODE]))
    cg.add(var.set_bit_order(config[CONF_BIT_ORDER]))
    await spi.register_spi_device(var, config)
    
