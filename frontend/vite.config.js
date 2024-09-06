import { defineConfig, loadEnv } from 'vite'
import path from 'path'
import createVitePlugins from './vite/plugins'

// https://vitejs.dev/config/
export default defineConfig(({ mode, command }) => {
    const env = loadEnv(mode, process.cwd())
        // const { VITE_APP_ENV } = env
    return {
        base: '/',
        server: {
            // host: '192.168.56.1', // 指定服务器的主机地址
            port: 8081,
            proxy: {
                '/api': {
                    target: 'http://localhost:5000',
                    changeOrigin: true,
                    ws: true,
                    secure: false,
                    logLevel: 'debug',
                    pathRewrite: {
                        '^/api': ''
                    }
                    // rewrite: (path) => path.replace(/^\/api/, '')
                }
            }
        },
        plugins: createVitePlugins(env, command === 'build'),
        resolve: {
            alias: {
                // 设置路径
                '~': path.resolve(__dirname, './'),
                // 设置别名
                '@': path.resolve(__dirname, './src')
            }
        },
        build: {
            // g6
            commonjsOptions: {
                ignoreTryCatch: false
            }
        }
    }
})