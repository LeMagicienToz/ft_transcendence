import React from 'react';
import { motion } from 'framer-motion';

const Typewriter = () => {
    // The text we want to animate
    const text = "FT_Transcendence";
  
    // Animation variants for each letter
    const letterAnimation = {
      hidden: { opacity: 0, y: 20 }, // Start with the letter below the baseline
      visible: {
        opacity: 1,
        y: 0, // Move letter to its final position
        transition: {
          duration: 8, // Duration for each letter animation
          type: "spring", // Smooth spring effect
        },
      },
    };
  
    return (
      <div style={{ display: 'flex', fontSize: '2em', fontFamily: 'monospace' }}>
        {text.split("").map((letter, index) => (
          <motion.span
            key={index}
            variants={letterAnimation}
            initial="hidden"
            animate="visible"
            custom={index}
            transition={{ delay: index * 8 }} // Delay each letter by 0.1s
          >
            {letter}
          </motion.span>
        ))}
      </div>
    );
  };
  
  export default Typewriter;