/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          // 更换为水墨绿色系，更自然温暖
          50: '#f2f7f5',
          100: '#e6f0eb',
          200: '#c3dbd0',
          300: '#9fc6b5',
          400: '#76b297',
          500: '#4d9d7a',
          600: '#3d7d62',
          700: '#2e5e49',
          800: '#1e3e31',
          900: '#0f1f18',
        },
        earth: {
          // 添加土色系，体现乡村质朴感
          50: '#faf8f3',
          100: '#f7f3ed',
          200: '#e8dfd3',
          300: '#d9cbb9',
          400: '#c0aa8e',
          500: '#a68b69',
          600: '#8b7355',
          700: '#6b5a42',
          800: '#4a3f2f',
          900: '#2a241c',
        },
        ink: {
          // 添加水墨色系
          50: '#fafafa',
          100: '#f5f5f5',
          200: '#e0e0e0',
          300: '#9e9e9e',
          400: '#616161',
          500: '#212121',
          600: '#1a1a1a',
          700: '#141414',
          800: '#0d0d0d',
          900: '#070707',
        },
        bamboo: {
          // 竹色系，增加自然感
          50: '#f7f9f2',
          100: '#eef3e5',
          200: '#d5e3c0',
          300: '#b8d199',
          400: '#9abd72',
          500: '#7ca64b',
          600: '#658a3c',
          700: '#4e6d2d',
          800: '#37501e',
          900: '#20330f',
        }
      },
      fontFamily: {
        // 添加更有中国风的字体
        sans: ['PingFang SC', 'Microsoft YaHei', 'Hiragino Sans GB', 'sans-serif'],
        serif: ['Noto Serif SC', 'SimSun', 'STSong', 'serif'],
        calligraphy: ['KaiTi', 'STKaiti', 'BiauKai', 'cursive'],
      },
      boxShadow: {
        // 更柔和的阴影，模拟水墨晕染效果
        'soft': '0 4px 12px rgba(0, 0, 0, 0.05)',
        'ink': '0 4px 8px rgba(0, 0, 0, 0.08)',
        'paper': '0 2px 8px rgba(0, 0, 0, 0.06)',
        'brush': '0 8px 24px rgba(0, 0, 0, 0.12)',
      },
      backgroundImage: {
        // 添加水墨纹理背景
        'ink-texture': "url('data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='0.02'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')",
        'paper-texture': "url('data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23f5f5f5' fill-opacity='0.3'%3E%3Cpath d='M0 0h100v100H0z'/%3E%3C/g%3E%3C/svg%3E')",
      },
      borderRadius: {
        'ink': '12px',
        'brush': '16px',
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      }
    },
  },
  plugins: [],
}