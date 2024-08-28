import postcss from "rollup-plugin-postcss";
import resolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import { babel } from "@rollup/plugin-babel";
import { terser } from "rollup-plugin-terser";

export default {
  input: "src/main.js",
  output: {
    file: "static/build/main.js",
    format: "iife",
    sourcemap: true,
  },
  plugins: [
    resolve(),
    commonjs(),
    babel({
      babelHelpers: "bundled",
      presets: ["@babel/preset-env"],
    }),
    terser(),
    postcss({
      extensions: [".css", ".scss"],
      extract: true, // or specify a path like 'dist/styles.css'
    }),
  ],
};
