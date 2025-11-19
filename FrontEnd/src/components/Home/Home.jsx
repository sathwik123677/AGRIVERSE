import React from "react";
import HeroImg from "../assets/1.jpg";
import Services from '../services/Services'

const Home = () => {
  const style = {
    backgroundImage: `url(${HeroImg})`,
    backgroundSize: "cover",
    backgroundRepeat: "no-repeat",
    backgroundPosition: "center",
  };

  return (<>
    <div className="h-screen flex flex-col justify-center px-[2rem] md:px-[4rem]" style={style}>
      <div className="text-green-600 text-2xl font-bold md:text-[5rem]">Agriverse</div>
      <div className="text-white text-xl md:text-[2rem] p-2 w-2/3 font-bold mt-5 md:mt-12">

      Agriverse is a platform that combines machine learning (ML) with agriculture. It uses advanced technology to improve farming practices, crop management, and decision-making processes for farmers.
</div>
    </div>
    <Services/>
    </>
  );
};

export default Home;
