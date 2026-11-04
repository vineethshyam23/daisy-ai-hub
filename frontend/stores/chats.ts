import { defineStore } from 'pinia'

// Helper functions
const generateUUID = () => {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
    var r = (Math.random() * 16) | 0,
      v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
};

const generateTimestamp = (date: Date) => {
  const day = date.getDate().toString().padStart(2, "0");
  const month = (date.getMonth() + 1).toString().padStart(2, "0");
  const year = date.getFullYear();
  const hours = date.getHours().toString().padStart(2, "0");
  const minutes = date.getMinutes().toString().padStart(2, "0");
  const seconds = date.getSeconds().toString().padStart(2, "0");
  return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`;
};

const randomAnswer = (type: 'opening' | 'error') => {
  const openings = [
    "Hello! How can I help you today?",
    "Hi there! I'm your AI assistant. How can I help you?",
    "Hey! Ready to help you with your questions. Let's go!",
  ];
  const errors = [
    "Sorry, I'm not sure about that. Could you try rephrasing your question?",
  ];

  const answers = type === 'opening' ? openings : errors;
  return answers[Math.floor(Math.random() * answers.length)];
};

export const useChatStore = defineStore('chat', {
  state: () => ({
    sessionId: generateUUID(),
    chatHistory: [
      {
        sender: 'AI',
        text: randomAnswer('opening'),
        time: generateTimestamp(new Date()),
        feedback: 'none',
      },
    ],
    currentUser: null as any,
    activeUserChat: {
      question: '',
      mode: 'text',
    },
    loading: false,
    version: '1.0',
    showModal: false,
    feedbackNote: '',
  }),

  actions: {
    async sendMessage(message: string) {
      if (message.trim() === '') return;

      // Add user message
      this.chatHistory.push({
        sender: 'YOU',
        text: message,
        time: generateTimestamp(new Date()),
        feedback: 'none',
      });

      this.loading = true;

      try {
        // Here you would make your API call
        // For now, we'll simulate a response
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        this.chatHistory.push({
          sender: 'AI',
          text: 'This is a sample response. Replace with actual API call.',
          time: generateTimestamp(new Date()),
          feedback: 'none',
        });
      } catch (error) {
        this.chatHistory.push({
          sender: 'AI',
          text: randomAnswer('error'),
          time: generateTimestamp(new Date()),
          feedback: 'none',
        });
      } finally {
        this.loading = false;
      }
    },

    async giveFeedback(feedback: 'positive' | 'negative', index: number, note: string = '') {
      if (this.chatHistory[index]) {
        this.chatHistory[index].feedback = feedback;
        // Here you would send feedback to your API
      }
    },

    clearChat() {
      this.chatHistory = [{
        sender: 'AI',
        text: randomAnswer('opening'),
        time: generateTimestamp(new Date()),
        feedback: 'none',
      }];
    },
  },
});