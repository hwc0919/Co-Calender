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
    // publicPath: 'http://localhost:5000',

    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:5000',
                pathRewrite: {
                    '/api': ''
                }
            }
        }
    }
};
