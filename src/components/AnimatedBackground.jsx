import React from "react";
import "../pages/Dashboard.css";

const AnimatedBackground = () => {
  return (
    <div className="animated-bg" aria-hidden>
      <div className="bg-orb orb1" />
      <div className="bg-orb orb2" />
      <div className="bg-orb orb3" />
    </div>
  );
};

export default AnimatedBackground;
