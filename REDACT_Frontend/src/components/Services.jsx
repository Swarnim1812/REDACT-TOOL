import Section from "./Section";
import Heading from "./Heading";
import { newbg } from "../assets";
import {
  PhotoChatMessage,
  Gradient,
} from "./design/Services";
import ChatFAQs from "./ChatFAQs";
import Button from "./Button";
import { NavLink } from "react-router-dom";

const Services = () => {
  return (
    <Section id="FAQs">
      <div className="container">
        <Heading
          title="FAQs and more"
          text="Learn more about RE-DACT’s capabilities and how it works."
        />
        <div className="relative">
          <div className="relative z-1 grid gap-5 lg:grid-cols-2">
            <div className="relative min-h-[39rem] border border-n-1/10 rounded-3xl overflow-hidden">
              <div className="absolute inset-0">
                <img
                  src={newbg}
                  className="h-full w-full object-cover opacity-40"
                  width={630}
                  height={750}
                  alt="robot"
                />
              </div>
              <div className="absolute inset-0 px-4 flex flex-col justify-end bg-gradient-to-b from-n-8/0 to-n-8/90 lg:p-10">
                <h5 className="h6 mb-1">Legal document and financial records Redaction:</h5>
                <p className="body-2 mb-[1rem] text-n-3">
                  Remove confidential details like names, addresses, case identifiers, and financial data.
                </p>
                {/* <h5 className="h6 mb-1">Financial Records:</h5>
                <p className="body-2 mb-[1rem] text-n-3">
                  Redact account numbers, transaction details, or other sensitive financial identifiers.
                </p> */}
                <h5 className="h6 mb-1">Research and Data Sharing:</h5>
                <p className="body-2 mb-[1rem] text-n-3">
                  Anonymize participant data for academic research or open datasets.
                </p>
                <h5 className="h6 mb-1">Machine Learning Training:</h5>
                <p className="body-2 mb-[1rem] text-n-3">
                  Create realistic synthetic datasets that preserve patterns for training without compromising privacy.
                </p>
                <h5 className="h6 mb-1">Video Redaction:</h5>
                <p className="body-2 mb-[1rem] text-n-3">
                  Blur faces and text in videos for legal, surveillance, or media purposes.
                </p>
              </div>

              <PhotoChatMessage />
            </div>

            <div className="p-2 bg-n-7 rounded-3xl overflow-hidden lg:min-h-[46rem]">
              <div className="py-5 px-4 xl:px-8">
                <h4 className="hover_target h4 mb-4">Frequently Asked Questions</h4>
              </div>

              <div className="relative h-[20rem] bg-none rounded-xl overflow-hidden md:h-[35rem]">
                <ChatFAQs />
              </div>
            </div>
          </div>

          <Gradient />
        </div>
        <div className="flex justify-center xl:mt-20">
          <NavLink to="/get-started">
            <Button><span className="hover_target ">GET STARTED</span></Button>
          </NavLink>
        </div>
      </div>
    </Section>
  );
};

export default Services;
