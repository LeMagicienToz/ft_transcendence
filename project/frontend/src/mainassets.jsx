import { motion } from "framer-motion";


function mot_button() {
    return (
      <motion.button
        whileTap={{ scale: 0.85 }}
      >
        Click me!
      </motion.button>
    );
  }
  
  export default mot_button;