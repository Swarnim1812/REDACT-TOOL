import React from 'react'
import Header from './Header'
import Hero from './Hero'
import Benefits from './Benefits'
import Collaboration from './Collaboration'
import Services from './Services'
import Footer from './Footer'

const Landingpage = () => {
  return (
    <div className="pt-[4.75rem] lg:pt-[5.25rem] overflow-hidden">
      <Header />
      <Hero />
      <Benefits />
      {/* <Collaboration /> */}
      <Services />
      <Footer />
    </div>
  )
}

export default Landingpage