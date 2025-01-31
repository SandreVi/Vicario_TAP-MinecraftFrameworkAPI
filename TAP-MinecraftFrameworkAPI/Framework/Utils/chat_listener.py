import time

class ChatListener:
    def __init__(self, mc):
        """
        Листенер хила охьал, Minecraft объект хьа мотт дац зе.
        :param mc: Minecraft оьрхан объект (техамкха, хьа мотт дац).
        """
        self.mc = mc

    def process_message(self, command):
        """
        Цуннаш функциеш, со гӀоацан къомандеш хила чат.
        """
        raise NotImplementedError("ГӀоацаш хила ещелах")

    def listen_for_chat_commands(self, agent, timeout_enabled, timeout):
        """
        Листенинг хила чат сообщенияш, и хила къомандеш зе максимал хьилда хи таймаут.
        Егер таймаут хила, агай хила къомандеш, че хиларда таймаут (если таймаут активирован).
        
        :param agent: Агент, со хила къомандеш
        :param timeout_enabled: Булиш, дац таймаут уьрхаша (дефолт хила True)
        :param timeout: Максимальн таймаут, хила къомандеш (дефолт хила 10 секунд)
        """
        if timeout_enabled:
            start_time = time.time()  # Лех хи вац хила тайм

        listening = True
        
        while listening:
            # Чат сообщенияш хила
            chat_messages = self.mc.events.pollChatPosts()

            if chat_messages:
                # Если сообщенияш лахан, со первых хила
                for message in chat_messages:

                    command = message.message
                    
                    # Листенинг цу дац, "STOP"/"stop" или "END"/"end" къомандаш
                    if command in ["STOP", "END", "stop", "end"]:
                        listening = False
                        break
                    
                    # Процесс къомандаш агент хила
                    agent.process_message(command)

                    if timeout_enabled:
                        start_time = time.time()  # Тайм хила, тик хи тайм после къомандеш

            # Проверка таймаут, если таймаут активирован
            if timeout_enabled:
                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout:
                    # Таймаут хила, со None къомандаш
                    agent.process_message(None)  
                    listening = False  # Листенинг цу дац, если таймаут хила
