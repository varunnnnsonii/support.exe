import { useState } from 'react'
import reactLogo from './assets/react.svg'
import Main from './components/Main'
import './index.css'; // or './globals.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <Main />
    </>
  )
}

export default App
