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
import './App.css';

function App() {
  // State Management of my Component
  const [userInput, setUserInput] = useState(''); // holds user message until I press send
  const [chatMessages, setChatMessages] = useState([]); // holds entire chat history variable and function it saves
  const[botResponse, setBotResponse] = useState(null); // response object is a
  // useEffect(() => { //calls the function on every reload
  //   sendMessage();
  // },[]) // a watcher, if I want to send something every time a variable changes, trigger the []

  const parentFunction = () => { 
    if (userInput.includes("zipcode:")) {
      sendMessageFDA('http://localhost:5000/fda')
    } else {
      sendMessage('http://localhost:5000/')
    }
  }

  const sendMessageFDA = (url) => {
    const messageData = {
      sender: 'You',
      message: userInput,
    }

    console.log(chatMessages)
    setChatMessages([...chatMessages, { sender: 'You', message: userInput }]);
    console.log(chatMessages)


    setUserInput('');
    fetch(url, { // holds flask server endpoint
    method: 'POST', //post request send data in it
    headers: {
      'Content-Type' : 'application/json'
    },
    body: JSON.stringify(messageData),
    })
    .then((response) => response.json())
    .then((response) => { // botResponse saves my bot backend
      // setBotResponse(response)

      //update chat messages if needed

      // setBotResponse([...botResponse, {sender: 'Bot', message: response}]);
      console.log(chatMessages)
      console.log("RESPONSE: ", response)

      setChatMessages([
        ...chatMessages,
        { sender: 'You', message: userInput },
        { sender: 'Bot', message: response }, // Assuming 'response' is the bot's message
      ]);      console.log(chatMessages)
      setUserInput('');
    })
    .catch((error) => {
      console.error('Error: ', error)
    });
  }
  
  const sendMessage = (url) => { // hook it up to a component so it sees it every time a button is pressed
    const messageData = {
      sender: 'You',
      message: userInput,
    };
    console.log(chatMessages)
    setChatMessages([...chatMessages, { sender: 'You', message: userInput }]);
    console.log(chatMessages)

     // ... means we don't have a double array
    setUserInput('');
    fetch(url, { // holds flask server endpoint
    method: 'POST', //post request send data in it
    headers: {
      'Content-Type' : 'application/json'
    },
    body: JSON.stringify(messageData),
  })
    .then((response) => response.json())
    .then((response) => { // botResponse saves my bot backend
      // setBotResponse(response)

      //update chat messages if needed

      // setBotResponse([...botResponse, {sender: 'Bot', message: response}]);
      console.log(chatMessages)
      console.log("RESPONSE: ", response)

      setChatMessages([
        ...chatMessages,
        { sender: 'You', message: userInput },
        { sender: 'Bot', message: response }, // Assuming 'response' is the bot's message
      ]);      console.log(chatMessages)
      setUserInput('');
    })
    .catch((error) => {
      console.error('Error: ', error)
    });
};

  return (
    
    <div id = "app" style = {appStyle}>
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
        <button style={buttonStyle} onClick={parentFunction}>
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


const appStyle = {
  backgroundColor: '#f0f8ff', // Light blue background color
  minHeight: '100vh', // Make sure the container takes up the full viewport height
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
};

const chatContainerStyle = {
  maxWidth: '400px',
  margin: '0 auto',
  padding: '20px',
  backgroundColor: '#fff',
  borderRadius: '5px',
  boxShadow: '0 0 10px rgba(0, 0, 0, 0.2)',
};

const chatBoxStyle = {
  border: '2px solid #ccc',
  padding: '15px',
  minHeight: '200px',
  maxHeight: '300px',
  overflowY: 'scroll',
  marginBottom: '10px',
};

const userInputStyle = {
  width: '100%',
  padding: '12px',
  border: '3px solid #ccc',
  borderRadius: '4px',
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

