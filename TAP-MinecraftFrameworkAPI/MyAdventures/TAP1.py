import mcpi.minecraft as minecraft
import mcpi.block as block

# Conectar al servidor de Minecraft en localhost
mc = minecraft.Minecraft.create()

# Obtener la posición del jugador
pos = mc.player.getTilePos()

# Colocar un bloque de piedra a la derecha del jugador
mc.setBlock(pos.x + 1, pos.y, pos.z, block.STONE.id)

# Colocar un bloque de tierra debajo del jugador
mc.setBlock(pos.x, pos.y - 1, pos.z, block.DIRT.id)

# Enviar un mensaje al chat de Minecraft
mc.postToChat("¡Hola, Minecraft!")
