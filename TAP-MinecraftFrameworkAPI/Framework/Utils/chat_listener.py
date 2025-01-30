import time

class ChatListener:
    def __init__(self, mc):
        """
        Initializes the listener by reusing the provided Minecraft instance.
        :param mc: Minecraft connection object (should be passed externally).
        """
        self.mc = mc

    def process_message(self, command):
        """
        This method must be overridden by subclasses that need to handle chat commands.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def listen_for_chat_commands(self, agent, timeout_enabled, timeout):
        """
        Listens for chat messages and processes the command received within a timeout.
        If no command is received within the specified timeout, it passes None (if timeout is enabled).
        
        :param agent: The agent that will process the commands.
        :param timeout_enabled: Boolean indicating whether to respect timeout or not (default is True).
        :param timeout: The maximum time to wait for a command (default is 10 seconds).
        """
        if timeout_enabled:
            start_time = time.time()  # Save the start time
            
        listening = True
        
        while listening:
            # Read the chat messages
            chat_messages = self.mc.events.pollChatPosts()

            if chat_messages:
                # If there are messages, process the first one
                for message in chat_messages:

                    command = message.message
                    
                    # Stop listening if "STOP"/"stop" or "END"/"end" is received
                    if command in ["STOP", "END", "stop", "end"]:
                        listening = False
                        break
                    
                    # Process the command by passing it to the agent
                    agent.process_message(command)

                    if timeout_enabled:
                        start_time = time.time()  # Reset the start time after processing a message

            # Check if the timeout period has passed, only if timeout_enabled is True
            if timeout_enabled:
                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout:
                    # Pass None if the timeout is reached
                    agent.process_message(None)  
                    listening = False  # Terminate the loop if the timeout has passed
