import {
  benefitIcon1,
  benefitIcon2,
  benefitIcon3,
  benefitIcon4,
  benefitImage2,
  privacy,
  scalability,
  adhar,
  scale,
  context,
  chromecast,
  disc02,
  discord,
  discordBlack,
  facebook,
  figma,
  file02,
  framer,
  homeSmile,
  instagram,
  notification2,
  notification3,
  notification4,
  notion,
  photoshop,
  plusSquare,
  protopie,
  raindrop,
  recording01,
  recording03,
  roadmap1,
  roadmap2,
  roadmap3,
  roadmap4,
  searchMd,
  slack,
  sliders04,
  telegram,
  twitter,
  yourlogo,
  TeamLogo2,
  github,
  linkedin,
  satorugojo,
  newbg,
} from "../assets";

export const navigation = [
  {
    id: "0",
    title: "HOME",
    url: "#hero",
  },
  {
    id: "1",
    title: "Features",
    url: "#features",
  },
  {
    id: "2",
    title: "FAQs",
    url: "#FAQs",
  }
];

export const heroIcons = [homeSmile, file02, searchMd, plusSquare];

export const notificationImages = [notification4, notification3, notification2];

export const companyLogos = [TeamLogo2, TeamLogo2, TeamLogo2, TeamLogo2, TeamLogo2];

export const brainwaveServices = [
  "Photo generating",
  "Photo enhance",
  "Seamless Integration",
];

export const brainwaveServicesIcons = [
  recording03,
  recording01,
  disc02,
  chromecast,
  sliders04,
];

export const roadmap = [
  {
    id: "0",
    title: "Text Redaction",
    text: "Allows you to upload documents like PDFs, word documents, plain text files, powerpoint presentations or images and redact sensitive information.",
    date: "1",
    status: "done",
    url: "/redact-doc",
    colorful: true,
    color: "red-100",
    btn_text : "REDACT TEXT"
  },
  {
    id: "1",
    title: "Video Redaction",
    text: "Effortlessly redact faces in videos, ensuring privacy and safeguarding identities with precision.",
    date: "2",
    status: "done",
    color : "red-200",
    url: "/Redact-Video",
    btn_text : "REDACT VIDEO"
  },
];

export const benefits = [
  {
    id: "0",
    title: "1. Privacy Protection",
    text: "Redact ensures that sensitive data, such as personally identifiable information (PII) or confidential content, is securely anonymized or removed, protecting individuals' and organizations' privacy.",
    backgroundUrl: "./src/assets/benefits/card-1.svg",
    iconUrl: benefitIcon1,
    imageUrl: newbg,
  },
  {
    id: "1",
    title: "2. Enhanced Data Security",
    text: "Reducing exposure to sensitive information minimizes risks of data breaches, misuse, or unauthorized access.",
    backgroundUrl: "./src/assets/benefits/card-2.svg",
    iconUrl: benefitIcon2,
    imageUrl: newbg,
    light: true,
  },
  {
    id: "2",
    title: "3. Redaction of GOVT IDs",
    text: "Tailored redaction rules to detect specific patterns  such as:Classified document labels.Government IDs like AADHAAR or PAN",
    backgroundUrl: "./src/assets/benefits/card-3.svg",
    iconUrl: benefitIcon3,
    imageUrl: newbg,
  },
  {
    id: "3",
    title: "4. User Definable Gradation scale",
    text: "Lets users quickly set the level of Redaction according to thier requirement on a pre-defined scale of 1(least)-10(most) sensitive.",
    backgroundUrl: "./src/assets/benefits/card-4.svg",
    iconUrl: benefitIcon4,
    imageUrl: newbg,
    light: true,
  },
  {
    id: "4",
    title: "5. Preserves Context:",
    text: "The use of realistic replacements (e.g., Faker-generated data) ensures that the text remains useful for analysis or testing, even after anonymization.",
    backgroundUrl: "./src/assets/benefits/card-5.svg",
    iconUrl: benefitIcon1,
    imageUrl: newbg,
  },
  {
    id: "5",
    title: "6. Scalability",
    text: "The implementation can handle large datasets efficiently, making it suitable for projects requiring bulk anonymization.",
    backgroundUrl: "./src/assets/benefits/card-6.svg",
    iconUrl: benefitIcon2,
    imageUrl: newbg,
  },
];
export const socials = [
  {
    id: "1",
    title: "Github",
    iconUrl: github,
    url: "https://github.com/Swarnim1812",
  },
  {
    id: "2",
    title: "LinkedIn",
    iconUrl: linkedin,
    url: "https://www.linkedin.com/in/swarnim-raj-496106260/",
  },
];
