import { useEffect, useState } from "react";
import { MouseParallax } from "react-just-parallax";

import PlusSvg from "../../assets/svg/PlusSvg";

export const Gradient = () => {
  return (
    <>
      <div className="relative z-1 h-6 mx-2.5 bg-n-11 shadow-xl rounded-b-[1.25rem] lg:h-6 lg:mx-8" />
      <div className="relative z-1 h-6 mx-6 bg-n-11/70 shadow-xl rounded-b-[1.25rem] lg:h-6 lg:mx-20" />
    </>
  );
};

export const BottomLine = () => {
  return (
    <>
      <div className="hidden absolute top-[55.25rem] left-10 right-10 h-0.25 bg-n-6 pointer-events-none xl:block" />

      <PlusSvg className="hidden absolute top-[54.9375rem] left-[2.1875rem] z-2 pointer-events-none xl:block" />

      <PlusSvg className="hidden absolute top-[54.9375rem] right-[2.1875rem] z-2 pointer-events-none xl:block" />
    </>
  );
};

const Rings = () => {
  return (
    <>
      <div className="absolute top-1/2 left-1/2 w-[65.875rem] aspect-square border border-n-2/10 rounded-full -translate-x-1/2 -translate-y-1/2" />
      <div className="absolute top-1/2 left-1/2 w-[51.375rem] aspect-square border border-n-2/10 rounded-full -translate-x-1/2 -translate-y-1/2" />
      <div className="absolute top-1/2 left-1/2 w-[36.125rem] aspect-square border border-n-2/10 rounded-full -translate-x-1/2 -translate-y-1/2" />
      <div className="absolute top-1/2 left-1/2 w-[23.125rem] aspect-square border border-n-2/10 rounded-full -translate-x-1/2 -translate-y-1/2" />
    </>
  );
};

// export const BackgroundCircles = ({ parallaxRef }) => {
//   const [mounted, setMounted] = useState(false);

//   useEffect(() => {
//     setMounted(true);
//   }, []);

//   return (
//     <div className="absolute -top-[42.375rem] left-1/2 w-[78rem] aspect-square border border-n-2/5 rounded-full -translate-x-1/2 md:-top-[38.5rem] xl:-top-[32rem]">
//       <Rings />

//       {/* Moving background colored circle balls */}
//       <MouseParallax strength={0.07} parallaxContainerRef={parallaxRef}>
//         <div className="absolute bottom-1/2 left-1/2 w-0.25 h-1/2 origin-bottom rotate-[46deg]">
//           <div
//             className={`w-2 h-2 -ml-1 -mt-36 bg-gradient-to-b from-[#DD734F] to-[#1A1A32] rounded-full transition-transform duration-500 ease-out ${
//               mounted ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
//             }`}
//           />
//         </div>

//         <div className="absolute bottom-1/2 left-1/2 w-0.25 h-1/2 origin-bottom -rotate-[56deg]">
//           <div
//             className={`w-4 h-4 -ml-1 -mt-32 bg-gradient-to-b from-[#DD734F] to-[#1A1A32] rounded-full transition-transform duration-500 ease-out ${
//               mounted ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
//             }`}
//           />
//         </div>

//         <div className="absolute bottom-1/2 left-1/2 w-0.25 h-1/2 origin-bottom rotate-[54deg]">
//           <div
//             className={`hidden w-4 h-4 -ml-1 mt-[12.9rem] bg-gradient-to-b from-[#B9AEDF] to-[#1A1A32] rounded-full xl:block transit transition-transform duration-500 ease-out ${
//               mounted ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
//             }`}
//           />
//         </div>

//         <div className="absolute bottom-1/2 left-1/2 w-0.25 h-1/2 origin-bottom -rotate-[65deg]">
//           <div
//             className={`w-3 h-3 -ml-1.5 mt-52 bg-gradient-to-b from-[#B9AEDF] to-[#1A1A32] rounded-full transition-transform duration-500 ease-out ${
//               mounted ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
//             }`}
//           />
//         </div>

//         <div className="absolute bottom-1/2 left-1/2 w-0.25 h-1/2 origin-bottom -rotate-[85deg]">
//           <div
//             className={`w-6 h-6 -ml-3 -mt-3 bg-gradient-to-b from-[#88E5BE] to-[#1A1A32] rounded-full transition-transform duration-500 ease-out ${
//               mounted ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
//             }`}
//           />
//         </div>

//         <div className="absolute bottom-1/2 left-1/2 w-0.25 h-1/2 origin-bottom rotate-[70deg]">
//           <div
//             className={`w-6 h-6 -ml-3 -mt-3 bg-gradient-to-b from-[#88E5BE] to-[#1A1A32] rounded-full transition-transform duration-500 ease-out ${
//               mounted ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
//             }`}
//           />
//         </div>
//       </MouseParallax>
//     </div>
//   );
// };



export const BackgroundCircles = ({ parallaxRef }) => {
  return (
    <div className="absolute -top-[42.375rem] left-1/2 w-[78rem] aspect-square border border-n-2/5 rounded-full -translate-x-1/2 md:-top-[38.5rem] xl:-top-[32rem]">
      <Rings />

      {/* Revolving background colored circle balls */}
      <div className="absolute w-full h-full overflow-hidden">
        <div className="absolute w-6 h-6 bg-gradient-to-b from-[#DD734F] to-[#1A1A32] rounded-full animate-revolveCircle1" />
        <div className="absolute w-6 h-6 bg-gradient-to-b from-[#88E5BE] to-[#1A1A32] rounded-full animate-revolveCircle2" />
        <div className="absolute w-3 h-3 bg-gradient-to-b from-[#B9AEDF] to-[#1A1A32] rounded-full animate-revolveCircle3" />
        <div className="absolute w-5 h-5 bg-gradient-to-b from-[#DD734F] to-[#1A1A32] rounded-full animate-revolveCircle4" />
        <div className="absolute w-5 h-5 bg-gradient-to-b from-[#DD734F] to-[#1A1A32] rounded-full animate-revolveCircle5" />
        <div className="absolute w-5 h-5 bg-gradient-to-b from-[#DD734F] to-[#1A1A32] rounded-full animate-revolveCircle6" />
      </div>

      <style jsx>{`
        @keyframes revolveCircle1 {
          0% {
            transform: rotate(0deg) translateX(190px) rotate(0deg);
          }
          100% {
            transform: rotate(360deg) translateX(190px) rotate(-360deg);
          }
        }

        @keyframes revolveCircle2 {
          0% {
            transform: rotate(0deg) translateX(300px) rotate(0deg);
          }
          100% {
            transform: rotate(360deg) translateX(300px) rotate(-360deg);
          }
        }

        @keyframes revolveCircle3 {
          0% {
            transform: rotate(0deg) translateX(420px) rotate(0deg);
          }
          100% {
            transform: rotate(360deg) translateX(420px) rotate(-360deg);
          }
        }

        @keyframes revolveCircle4 {
          0% {
            transform: rotate(0deg) translateX(530px) rotate(0deg);
          }
          100% {
            transform: rotate(360deg) translateX(530px) rotate(-360deg);
          }
        }
        @keyframes revolveCircle5 {
          0% {
            transform: rotate(0deg) translateX(660px) rotate(0deg);
          }
          100% {
            transform: rotate(360deg) translateX(660px) rotate(-360deg);
          }
        }
        @keyframes revolveCircle6 {
          0% {
            transform: rotate(0deg) translateX(730px) rotate(0deg);
          }
          100% {
            transform: rotate(360deg) translateX(730px) rotate(-360deg);
          }
        }

        .animate-revolveCircle1 {
          position: absolute;
          top: 50%;
          left: 50%;
          animation: revolveCircle1 8s infinite linear;
          transform-origin: center;
          animation-delay: 1s;
        }

        .animate-revolveCircle2 {
          position: absolute;
          top: 50%;
          left: 50%;
          animation: revolveCircle2 8s infinite linear;
          transform-origin: center;
          animation-delay: 2s;
        }

        .animate-revolveCircle3 {
          position: absolute;
          top: 50%;
          left: 50%;
          animation: revolveCircle3 10s infinite linear;
          transform-origin: center;
          animation-delay: 3s;
        }

        .animate-revolveCircle4 {
          position: absolute;
          top: 50%;
          left: 50%;
          animation: revolveCircle4 10s infinite linear;
          transform-origin: center;
          animation-delay: 3s;
        }
        .animate-revolveCircle5 {
          position: absolute;
          top: 50%;
          left: 50%;
          animation: revolveCircle4 9s infinite linear;
          transform-origin: center;
          animation-delay: 3s;
        }
        .animate-revolveCircle6 {
          position: absolute;
          top: 50%;
          left: 50%;
          animation: revolveCircle4 10s infinite linear;
          transform-origin: center;
          animation-delay: 6s;
        }
      `}</style>
    </div>
  );
};
