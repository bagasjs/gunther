import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from "node:path"

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    publicDir: "../resources/templates/",
    build: {
        rollupOptions: {
            input: resolve(__dirname, "index.html"),
            output: {
                assetFileNames: "static/[name].[ext]",
                entryFileNames: "static/[name].js",
                chunkFileNames: 'static/[name].js',
            }
        },
        outDir: "../resources/",
        emptyOutDir: true,
    },
})
