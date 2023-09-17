// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;

import React, { useState, useEffect } from 'react';

function App() {
  // State Management of my Component
  const [userInput, setUserInput] = useState(''); // holds user message until I press send
  const [chatMessages, setChatMessages] = useState([]); // holds entire chat history variable and function it saves
  const[botResponse, setBotResponse] = useState(null); // response object is a
  // useEffect(() => { //calls the function on every reload
  //   sendMessage();
  // },[]) // a watcher, if I want to send something every time a variable changes, trigger the []

  const sendMessage = () => { // hook it up to a component so it sees it every time a button is pressed
    const messageData = {
      sender: 'You',
      message: userInput,
    };
    console.log(chatMessages)
    setChatMessages([...chatMessages, { sender: 'You', message: userInput }]);
    console.log(chatMessages)

     // ... means we don't have a double array
    setUserInput('');
    fetch('http://localhost:5000', { // holds flask server endpoint
    method: 'POST', //post request send data in it
    headers: {
      'Content-Type' : 'application/json'
    },
    body: JSON.stringify(messageData),
  })
    .then((response) => response.json())
    .then((response) => { // botResponse saves my bot backend
      setBotResponse(response)

      //update chat messages if needed

      // setBotResponse([...botResponse, {sender: 'Bot', message: response}]);
      console.log(chatMessages)

      setChatMessages([
        ...chatMessages,
        { sender: 'You', message: userInput },
        { sender: 'easytrials bot', message: response }, // Assuming 'response' is the bot's message
      ]);      console.log(chatMessages)
      setUserInput('');
    })
    .catch((error) => {
      console.error('Error: ', error)
    });
  
};

// const sendMessage = (messageData) => {
//   fetch('/', {
//     method: 'POST', // Use the appropriate HTTP method (e.g., POST)
//     headers: {
//       'Content-Type': 'application/json', // Set the appropriate content type
//     },
//     body: JSON.stringify(messageData), // Convert the data to JSON
//   })
//     .then((response) => {
//       if (!response.ok) {
//         throw new Error('Network response was not ok');
//       }
//       return response.json(); // If you expect a JSON response
//     })
//     .then((data) => {
//       // Handle the response from the server if needed
//       console.log('Server response:', data);
//     })
//     .catch((error) => {
//       // Handle errors
//       console.error('Error:', error);
//     });
// };


  //   fetch('/request', { // add full url
  //     method: 'POST', //post request send data in it
  //     body: new URLSearchParams({ user_input: userInput }), // how to create json from body in python
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //   })
  //     .then(response => response.json())
  //     .then(botResponse => { // botResponse saves my bot backend
  //       setChatMessages([...chatMessages, { sender: 'Bot', message: botResponse }]);
  //     });
  // };

  return (
    <div>
      <h1 align = "center">easytrials bot</h1>
      <div id="chat-container" style={chatContainerStyle}>
        <div id="chat-box" style={chatBoxStyle}>
          {chatMessages.map((message, index) => (
            <p key={index}>
              <strong>{message.sender}: {message.message}</strong>
            </p>
          ))}
          {/* {botResponse.map((message,index) => (
            <p key ={index}>
              <strong>{message.sender}: {message.message}</strong>
            </p>
          )
          )} */}
        </div>
        <input
          type="text"
          id="user-input"
          placeholder="Type your message..."
          style={userInputStyle}
          value={userInput}
          onChange={e => setUserInput(e.target.value)}
        />
        <button style={buttonStyle} onClick={sendMessage}>
          Send
        </button>
      </div>

      {/* {botResponse && (
        <div>
          <p> Bot Response: </p>
          <p> {botResponse} </p>
          </div>
      )} */}
    </div>
  );
}

const chatContainerStyle = {
  maxWidth: '400px',
  margin: '0 auto',
  padding: '20px',
  backgroundColor: '#fff',
  borderRadius: '5px',
  boxShadow: '0 0 10px rgba(0, 0, 0, 0.2)',
};

const chatBoxStyle = {
  border: '1px solid #ccc',
  padding: '10px',
  minHeight: '200px',
  maxHeight: '300px',
  overflowY: 'scroll',
  marginBottom: '10px',
};

const userInputStyle = {
  width: '100%',
  padding: '10px',
  border: '1px solid #ccc',
  borderRadius: '5px',
  marginBottom: '10px',
};

const buttonStyle = {
  backgroundColor: '#0074cc',
  color: '#fff',
  border: 'none',
  padding: '10px 20px',
  cursor: 'pointer',
  borderRadius: '5px',
};

export default App;

