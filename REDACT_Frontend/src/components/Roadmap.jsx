import Button from "./Button";
import Heading from "./Heading";
import Section from "./Section";
import Tagline from "./Tagline";
import { roadmap } from "../constants";
import { check2, grid, loading1 } from "../assets";
import { Gradient } from "./design/Roadmap";
import { NavLink } from "react-router-dom";
import { GoArrowRight } from "react-icons/go";
import { Link } from "react-router-dom";

const Roadmap = () => (
  <Section className=" h-screen" id="roadmap">
    <div className="container md:pb-10">
      <Heading tag="Ready to get started" title="Choose Your File Format" />

      <div className="relative grid gap-2 md:grid-cols-2 md:gap-4 md:pb-[1rem]">
        {roadmap.map((item) => {
          const status = item.status === "done" ? "Done" : "In progress";

          return (
            <div
              className={`md:flex even:md:translate-y-[4rem] p-0.25 rounded-[2.5rem] ${
                item.colorful ? "bg-conic-gradient" : "bg-n-6"
              }`}
              key={item.id}
            >
              <div className="relative p-8 bg-n-8 rounded-[2.4375rem] overflow-hidden xl:p-15">
                <div className="absolute top-0 left-0 max-w-full">
                  <img
                    className="w-full"
                    src={grid}
                    width={550}
                    height={550}
                    alt="Grid"
                  />
                </div>
                <div className="relative z-1 h-[22rem] flex flex-col ">
                  <div className="flex items-center justify-between max-w-[27rem] mb-8 md:mb-20">
                    <Tagline>{item.date}</Tagline>

                    <div className="flex items-center px-4 py-1 bg-n-1 rounded text-n-8">
                      <img
                        className="mr-2.5"
                        src={item.status === "done" ? check2 : loading1}
                        width={16}
                        height={16}
                        alt={status}
                      />
                      <div className="tagline">{status}</div>
                    </div>
                  </div>

                  <div className="mb-10 -my-10 -mx-15 h-[12rem] flex items-center justify-center">
                    <NavLink to ={item.url}>
                      <button type="button" className={`text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 
                        hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 shadow-lg shadow-blue-500/50 dark:shadow-lg dark:shadow-blue-800/80 font-[40px] rounded-xl text-sm px-[1em] py-6 text-center me-2 mb-2 w-[17em] flex items-center justify-center font-bold`}>{item.btn_text}<GoArrowRight className="ml-3 text-2xl"/></button>
                    </NavLink>
                  </div>
                  <h4 className="h4 mb-4">{item.title}</h4>
                  <p className="body-2 text-n-4">{item.text}</p>
                </div>
              </div>
            </div>
          );
        })}

        <Gradient />
      </div>

      <div className="flex justify-center mt-12 md:mt-15 xl:mt-20">
        <NavLink to="/"><Button>BACK TO HOME</Button></NavLink>

      </div>
    </div>
  </Section>
);

export default Roadmap;
