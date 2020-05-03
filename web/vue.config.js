module.exports = {
    configureWebpack: {
        resolve: { extensions: ['.ts', '.tsx', '.js', '.json'] },
        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    loader: 'ts-loader',
                    exclude: /node_modules/,
                    options: {
                        appendTsSuffixTo: [/\.vue$/]
                    }
                }
            ]
        }
    },

    devServer: {
        proxy: {
            '/api': {
                target: 'http://192.168.0.105:5000',
                pathRewrite: {
                    '/api': ''
                },
                changeOrigin: true
            }
        }
    }
};
