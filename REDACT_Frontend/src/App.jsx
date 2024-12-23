// import ButtonGradient from "./assets/svg/ButtonGradient";
// import Allroutes from "./components/Allroutes";
// // import Benefits from "./components/Benefits";
// // import Collaboration from "./components/Collaboration";
// // import Footer from "./components/Footer";
// // import Header from "./components/Header";
// // import Hero from "./components/Hero";
// // import Pricing from "./components/Pricing";
// // import Roadmap from "./components/Roadmap";
// // import Services from "./components/Services";
// // import StartingPage from "./components/StartingPage";

// const App = () => {
//   return (
//     <>
//       <Allroutes />
//       <ButtonGradient />
//     </>
//   );
// };

// export default App;


import React, { useState } from "react";
import ButtonGradient from "./assets/svg/ButtonGradient";
import Allroutes from "./components/Allroutes";
import Loader from "./components/Loader";
import CustomCursor from "./components/CustomCursor";
const App = () => {
  const [isLoading, setIsLoading] = useState(true);

  const handleLoadComplete = () => {
    setIsLoading(false); // Hide loader after loading
  };

  return (
    <>
      {isLoading ? (
        <Loader onLoadComplete={handleLoadComplete} />
      ) : (
        <>
          <CustomCursor />
          <Allroutes />
          <ButtonGradient />
        </>
      )}
    </>
  );
};

export default App;
