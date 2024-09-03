
import React from 'react';
import { motion } from 'framer-motion';

const Typewriter = () => {
  // The text we want to animate
  const text = "Ft_Transcendence";

  return (
    <div style={{ display: 'flex', fontSize: '2em', fontFamily: 'monospace' }}>
      {text.split("").map((letter, index) => (
        <motion.span
          key={index}
          initial={{ opacity: 0, y: 80 }} // Start below the baseline and hidden
          animate={{ opacity: 1, y: 0 }} // Animate to final position
          transition={{
            delay: index * 0.2, // Delay each letter by 0.2s multiplied by its index
            duration: 1, // Animation duration for each letter
            type: "spring", // Smooth spring effect
          }}
        >
          {letter}
        </motion.span>
      ))}
    </div>
  );
};

export default Typewriter;

  