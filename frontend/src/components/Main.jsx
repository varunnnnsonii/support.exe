

// // // export default Main;
// // import React, { useState, useRef, useEffect } from 'react';
// // import { assets } from '/src/assets/assets.js';

// // // Loader component
// // const Loader = () => (
// //   <div className="flex space-x-1">
// //     <div className="h-2 w-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0s' }} />
// //     <div className="h-2 w-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
// //     <div className="h-2 w-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
// //   </div>
// // );

// // // API call function
// // const sendapi = async (query, user_id, thread_id) => {
// //   try {
// //     const response = await fetch("http://127.0.0.1:8000/chat", {
// //       method: "POST",
// //       headers: { "Content-Type": "application/json" },
// //       body: JSON.stringify({ user_id, thread_id, message: query }),
// //     });

// //     const data = await response.json();
// //     return data.response;
// //   } catch (error) {
// //     console.error("Error:", error);
// //     return "There was an error communicating with the chatbot.";
// //   }
// // };

// // // Main Component
// // const Main = () => {
// //   const [input, setInput] = useState("");
// //   const [messages, setMessages] = useState([]);
// //   const [isLoading, setIsLoading] = useState(false);
// //   const bottomRef = useRef(null);

// //   // User and thread IDs as state
// //   const [userId] = useState("user123");
// //   const [threadId] = useState("thread123");

// //   // Scroll to bottom when messages change or loading state changes
// //   useEffect(() => {
// //     bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
// //   }, [messages, isLoading]);

// //   const sendMessage = async () => {
// //     if (!input.trim()) return;

// //     const userMsg = { sender: "user", text: input };
// //     setMessages(prev => [...prev, userMsg]);
// //     setIsLoading(true);
// //     const currentInput = input;
// //     setInput("");

// //     try {
// //       const response = await sendapi(currentInput, userId, threadId);
// //       const agentMsg = { sender: "agent", text: response };
// //       setMessages(prev => [...prev, agentMsg]);
// //     } catch {
// //       setMessages(prev => [...prev, { sender: "agent", text: "Sorry, something went wrong." }]);
// //     } finally {
// //       setIsLoading(false);
// //     }
// //   };

// //   return (
// //     <div className="h-screen w-screen bg-white flex flex-col">
// //       {/* Navbar */}
// //       <header className="bg-white p-4 flex justify-between items-center shadow">
// //         <p className="font-sans text-lg font-semibold text-gray-700">CustomerCare</p>
// //         <img src="" alt="Logo" className="w-8 h-8 bg-blue-400 rounded-full" />
// //       </header>

// //       {/* Chat Container */}
// //       <div className="flex-1 flex flex-col overflow-hidden">
// //         {/* Messages Area */}
// //         <div className="flex-1 overflow-y-auto p-4 space-y-2 scrollbar-hidden">
// //           {messages.map((msg, index) => (
// //             <div key={index} className={`flex ${msg.sender === 'agent' ? 'justify-start' : 'justify-end'}`}>
// //               <div
// //                 className={`font-sans text-lg px-4 py-3 rounded-lg max-w-[70%] break-words overflow-y-auto ${msg.sender === 'agent' ? 'bg-blue-50 text-black' : 'bg-white text-black'}`}
// //                 style={{ maxHeight: '70vh' }}
// //               >
// //                 {msg.text}
// //               </div>
// //             </div>
// //           ))}

// //           {/* Loader */}
// //           {isLoading && (
// //             <div className="flex justify-start">
// //               <div className="bg-blue-50 p-4 rounded-lg max-w-[70%]">
// //                 <Loader />
// //               </div>
// //             </div>
// //           )}

// //           {/* Dummy div to scroll into view */}
// //           <div ref={bottomRef} />
// //         </div>

// //         {/* Input Area */}
// //         <div className="sticky bottom-0 bg-white p-4 border-t border-gray-200">
// //           <div className="flex items-center gap-2">
// //             <input
// //               value={input}
// //               onChange={e => setInput(e.target.value)}
// //               type="text"
// //               placeholder="Type your message here..."
// //               className="font-sans flex-1 p-2 text-black rounded-xl outline-none bg-gray-50"
// //             />
// //             <button
// //               onClick={sendMessage}
// //               disabled={isLoading}
// //               className="p-2 bg-blue-500 text-white rounded-full disabled:opacity-50 focus:outline-none focus:ring-2 focus:ring-blue-300"
// //             >
// //               <img className="h-6 w-6" src={assets.send_icon} alt="Send" />
// //             </button>
// //           </div>
// //           <p className="font-sans text-sm text-gray-500 mt-1 text-center">
// //             AI can make mistakes, so double-check it
// //           </p>
// //         </div>
// //       </div>
// //     </div>
// //   );
// // };

// // export default Main;
// import React, { useState, useRef, useEffect } from 'react';
// import { assets } from '/src/assets/assets.js';

// // Loader component
// const Loader = () => (
//   <div className="flex space-x-1">
//     <div className="h-2 w-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0s' }} />
//     <div className="h-2 w-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
//     <div className="h-2 w-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
//   </div>
// );

// // API call function
// const sendapi = async (query, user_id, thread_id) => {
//   try {
//     const response = await fetch("http://127.0.0.1:8000/chat", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ user_id, thread_id, message: query }),
//     });

//     const data = await response.json();
//     return data.response;
//   } catch (error) {
//     console.error("Error:", error);
//     return "There was an error communicating with the chatbot.";
//   }
// };

// // Main Component
// const Main = () => {
//   const [input, setInput] = useState("");
//   const [messages, setMessages] = useState([]);
//   const [isLoading, setIsLoading] = useState(false);
//   const bottomRef = useRef(null);

//   // User and thread IDs as state
//   const [userId] = useState("user123");
//   const [threadId] = useState("thread123");

//   // Scroll to bottom when messages change or loading state changes
//   useEffect(() => {
//     bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
//   }, [messages, isLoading]);

//   const sendMessage = async () => {
//     if (!input.trim()) return;

//     const userMsg = { sender: "user", text: input };
//     setMessages(prev => [...prev, userMsg]);
//     setIsLoading(true);
//     const currentInput = input;
//     setInput("");

//     try {
//       const response = await sendapi(currentInput, userId, threadId);
//       const agentMsg = { sender: "agent", text: response };
//       setMessages(prev => [...prev, agentMsg]);
//     } catch {
//       setMessages(prev => [...prev, { sender: "agent", text: "Sorry, something went wrong." }]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   return (
//     <div className="h-screen w-screen bg-white flex flex-col">
//       {/* Navbar */}
//       <header className="bg-white p-4 flex justify-between items-center shadow">
//         <p className="font-sans text-lg font-semibold text-gray-700">CustomerCare</p>
//         <img src="" alt="Logo" className="w-8 h-8 bg-blue-400 rounded-full" />
//       </header>

//       {/* Main Content */}
//       <main className="flex-1 flex justify-center bg-white">
//         {/* Chat Wrapper: 50% width */}
//         <div className="w-1/2 h-full flex flex-col overflow-hidden shadow-lg rounded-lg">
//           {/* Messages Area */}
//           <div className="flex-1 overflow-y-auto p-4 space-y-2 scrollbar-thin scrollbar-thumb-gray-400">
//             {messages.map((msg, index) => (
//               <div key={index} className={`flex ${msg.sender === 'agent' ? 'justify-start' : 'justify-end'}`}>
//                 <div
//                   className={`font-sans text-lg px-4 py-3 rounded-lg max-w-[70%] break-words overflow-y-auto ${msg.sender === 'agent' ? 'bg-blue-50 text-black' : 'bg-white text-black'}`}
//                   style={{ maxHeight: '70vh' }}
//                 >
//                   {msg.text}
//                 </div>
//               </div>
//             ))}

//             {/* Loader */}
//             {isLoading && (
//               <div className="flex justify-start">
//                 <div className="bg-blue-50 p-4 rounded-lg max-w-[70%]">
//                   <Loader />
//                 </div>
//               </div>
//             )}

//             {/* Dummy div to scroll into view */}
//             <div ref={bottomRef} />
//           </div>

//           {/* Input Area */}
//           <div className="sticky bottom-0 bg-white p-4 border-t border-gray-200">
//             <div className="flex items-center gap-2">
//               <input
//                 value={input}
//                 onChange={e => setInput(e.target.value)}
//                 type="text"
//                 placeholder="Type your message here..."
//                 className="font-sans flex-1 p-2 text-black rounded-xl outline-none bg-gray-50"
//               />
//               <button
//                 onClick={sendMessage}
//                 disabled={isLoading}
//                 className="p-2 bg-blue-500 text-white rounded-full disabled:opacity-50 focus:outline-none focus:ring-2 focus:ring-blue-300"
//               >
//                 <img className="h-6 w-6" src={assets.send_icon} alt="Send" />
//               </button>
//             </div>
//             <p className="font-sans text-sm text-gray-500 mt-1 text-center">
//               AI can make mistakes, so double-check it
//             </p>
//           </div>
//         </div>
//       </main>
//     </div>
//   );
// };

// export default Main;
import React, { useState, useRef, useEffect } from 'react';
import { assets } from '/src/assets/assets.js';

// Loader component
const Loader = () => (
  <div className="flex space-x-1">
    <div className="h-2 w-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0s' }} />
    <div className="h-2 w-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
    <div className="h-2 w-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
  </div>
);

// API call function
const sendapi = async (query, user_id, thread_id) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id, thread_id, message: query }),
    });

    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error("Error:", error);
    return "There was an error communicating with the chatbot.";
  }
};

// Main Component
const Main = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef(null);

  // User and thread IDs as state
  const [userId] = useState("user123");
  const [threadId] = useState("thread123");

  // Scroll to bottom when messages change or loading state changes
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);
    const currentInput = input;
    setInput("");

    try {
      const response = await sendapi(currentInput, userId, threadId);
      const agentMsg = { sender: "agent", text: response };
      setMessages(prev => [...prev, agentMsg]);
    } catch {
      setMessages(prev => [...prev, { sender: "agent", text: "Sorry, something went wrong." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-screen w-screen bg-white flex flex-col overflow-hidden">
      {/* Navbar */}
      <header className="bg-white p-4 flex justify-between items-center shadow">
        <p className="font-sans text-lg font-semibold text-gray-700">CustomerCare</p>
        <img src="" alt="Logo" className="w-8 h-8 bg-blue-400 rounded-full" />
      </header>

      {/* Main Content */}
      <main className="flex-1 flex justify-center bg-white overflow-hidden">
        {/* Chat Wrapper: 50% width */}
        <div className="w-1/3 h-full flex flex-col overflow-hidden shadow-lg rounded-lg">
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-2 scrollbar-hidden ">
            {messages.map((msg, index) => (
              <div key={index} className={`flex ${msg.sender === 'agent' ? 'justify-start' : 'justify-end'}`}>
                <div
                  className={`font-sans text-lg px-4 py-3 rounded-lg max-w-[70%] break-words overflow-y-auto ${msg.sender === 'agent' ? 'bg-blue-50 text-black' : 'bg-white text-black'}`}
                  style={{ maxHeight: '70vh' }}
                >
                  {msg.text}
                </div>
              </div>
            ))}

            {/* Loader */}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-blue-50 p-4 rounded-lg max-w-[70%]">
                  <Loader />
                </div>
              </div>
            )}

            {/* Dummy div to scroll into view */}
            <div ref={bottomRef} />
          </div>

          {/* Input Area */}
          <div className="sticky bottom-0 bg-white p-4 border-t border-gray-200">
            <div className="flex items-center gap-2">
              <input
                value={input}
                onChange={e => setInput(e.target.value)}
                type="text"
                placeholder="Type your message here..."
                className="font-sans flex-1 p-2 text-black rounded-xl outline-none bg-gray-50"
              />
              <button
                onClick={sendMessage}
                disabled={isLoading}
                className="p-2 bg-blue-500 text-white rounded-full disabled:opacity-50 focus:outline-none focus:ring-2 focus:ring-blue-300"
              >
                <img className="h-6 w-6" src={assets.send_icon} alt="Send" />
              </button>
            </div>
            <p className="font-sans text-sm text-gray-500 mt-1 text-center">
              AI can make mistakes, so double-check it
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Main;
