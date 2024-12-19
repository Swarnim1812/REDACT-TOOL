import React from 'react'
import StartingPage from './StartingPage'
import Landingpage from './Landingpage'
import { BrowserRouter, Routes, Route} from 'react-router-dom'
import Redact_doc from './Redact_doc'
import Redact_Video from './Redact_Video'

const Allroutes = () => {
  return (
      <Routes>
        <Route path='/' element={<Landingpage />} />
        <Route path='/get-started' element={<StartingPage />} />
        <Route path='/redact-doc' element={<Redact_doc />} />
        <Route path='/Redact-Video' element={<Redact_Video />} />
      </Routes>
  )
}
export default Allroutes