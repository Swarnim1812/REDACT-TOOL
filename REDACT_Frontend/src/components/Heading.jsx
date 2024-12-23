import TagLine from "./Tagline";

const Heading = ({ className, title, text, tag }) => {
  return (
    <div className={`${className} hover_target max-w-[50rem] mx-auto mb-12 lg:mb-20 md:text-center`}>
      {tag && <TagLine className="hover_target mb-4 md:justify-center">{tag}</TagLine>}
      {title && <h2 className="hover_target h2">{title}</h2>}
      {text && <p className="hover_target body-2 mt-4 text-n-4">{text}</p>}
    </div>
  );
};

export default Heading;
