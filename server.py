<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Grok Chat Interface</title>
  <script src="https://cdn.jsdelivr.net/npm/react@18.2.0/umd/react.production.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/react-dom@18.2.0/umd/react-dom.production.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@babel/standalone@7.20.6/babel.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/socket.io-client@4.5.1/dist/socket.io.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
      background-color: #f5f5f5;
    }
    #root {
      height: 100vh;
      display: flex;
    }
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    const { useState, useEffect } = React;

    const ChatMessage = ({ message, isUser }) => (
      <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 px-4`}>
        <div
          className={`max-w-[70%] p-3 rounded-lg shadow ${
            isUser ? 'bg-blue-500 text-white' : 'bg-white text-gray-800'
          }`}
        >
          {message}
        </div>
      </div>
    );

    const Sidebar = ({ conversations, onSelectConversation, onNewChat }) => (
      <div className="w-full md:w-64 bg-gray-800 text-white h-full p-4 flex flex-col">
        <h2 className="text-lg font-semibold mb-4">Conversations</h2>
        <div className="flex-1 overflow-y-auto">
          {conversations.map((conv, index) => (
            <div
              key={index}
              className="p-2 mb-2 rounded-lg hover:bg-gray-700 cursor-pointer"
              onClick={() => onSelectConversation(index)}
            >
              Conversation {index + 1}
            </div>
          ))}
        </div>
        <button
          className="mt-4 bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded"
          onClick={onNewChat}
        >
          New Chat
        </button>
      </div>
    );

    const ChatInterface = () => {
      const [messages, setMessages] = useState([
        { text: 'Hello! How can I assist you today?', isUser: false },
      ]);
      const [input, setInput] = useState('');
      const [conversations, setConversations] = useState([[]]);
      const [currentConversation, setCurrentConversation] = useState(0);
      const [isSidebarOpen, setIsSidebarOpen] = useState(false);
      const [socket, setSocket] = useState(null);

      useEffect(() => {
        // Initialize WebSocket connection
        const newSocket = io('http://localhost:5000');
        setSocket(newSocket);

        // Listen for bot responses
        newSocket.on('bot_response', (data) => {
          const newMessages = [...messages, { text: data.response, isUser: false }];
          setMessages(newMessages);
          setConversations((prev) => {
            const updated = [...prev];
            updated[currentConversation] = newMessages;
            return updated;
          });
        });

        return () => newSocket.disconnect();
      }, [messages, currentConversation]);

      const handleSend = () => {
        if (input.trim() && socket) {
          const newMessages = [...messages, { text: input, isUser: true }];
          setMessages(newMessages);
          setConversations((prev) => {
            const updated = [...prev];
            updated[currentConversation] = newMessages;
            return updated;
          });
          socket.emit('user_message', { message: input });
          setInput('');
        }
      };

      const handleNewChat = () => {
        setMessages([{ text: 'Hello! How can I assist you today?', isUser: false }]);
        setConversations((prev) => [...prev, []]);
        setCurrentConversation(conversations.length);
        setIsSidebarOpen(false);
      };

      const handleSelectConversation = (index) => {
        setCurrentConversation(index);
        setMessages(
          conversations[index].length
            ? conversations[index]
            : [{ text: 'Hello! How can I assist you today?', isUser: false }]
        );
        setIsSidebarOpen(false);
      };

      return (
        <div className="flex w-full h-full">
          {/* Sidebar */}
          <div
            className={`fixed md:static inset-0 z-50 bg-gray-800 transform ${
              isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
            } md:translate-x-0 transition-transform duration-300 ease-in-out md:w-64`}
          >
            <Sidebar
              conversations={conversations}
              onSelectConversation={handleSelectConversation}
              onNewChat={handleNewChat}
            />
          </div>

          {/* Main Chat Area */}
          <div className="flex-1 flex flex-col h-full">
            {/* Header */}
            <div className="bg-white shadow p-4 flex items-center justify-between">
              <div className="flex items-center">
                <button
                  className="md:hidden text-gray-600"
                  onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-7 6h7" />
                  </svg>
                </button>
                <h1 className="text-xl font-semibold ml-2">Grok Chat</h1>
              </div>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-4 bg-gray-100">
              {messages.map((msg, index) => (
                <ChatMessage key={index} message={msg.text} isUser={msg.isUser} />
              ))}
            </div>

            {/* Input Area */}
            <div className="bg-white p-4 shadow-inner">
              <div className="flex items-center max-w-3xl mx-auto">
                <textarea
                  className="flex-1 p-2 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows="2"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSend())}
                  placeholder="Type your message..."
                />
                <button
                  className="ml-2 bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-lg"
                  onClick={handleSend}
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    };

    ReactDOM.render(<ChatInterface />, document.getElementById('root'));
  </script>
</body>
</html>
<xaiArtifact artifact_id="d4f2504c-00c2-432b-ba9b-b9be0970071e" artifact_version_id="ec423d8a-5a23-4e4a-b6a1-5493a97318ec" title="server.py" contentType="text/python">
from flask import Flask, request
from flask_socketio import SocketIO, emit
from hugchat import hugchat

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize HugChat chatbot
chatbot = hugchat.ChatBot()

@socketio.on('user_message')
def handle_message(data):
    user_input = data['message']
    try:
        # Get response from HugChat
        response = chatbot.chat(user_input)
        emit('bot_response', {'response': response})
    except Exception as e:
        emit('bot_response', {'response': f'Error: {str(e)}'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
