# 📊 Esport-statistics

This website provides a comprehensive collection of statistics and comparisons on various esports games. The site gathers its data from Liquipedia and presents it in an easily accessible and understandable format.

**Authors :** [Arthur ALLAIN](https://github.com/Pataubeur) and [Romain BRIEND](https://github.com/yami2200)

**Link :** [Website](https://esport-statistics.vercel.app/)

## 📂 Project Structure

```
📦esports-statistics
 ┣ 📂public               // Static assets (icon, images...)
 ┣ 📂scripts              // Scripts to gather data from Liquipedia and generate JSON files
 ┃ ┗ 📜main.py            // Main script to run
 ┣ 📂src                  // Source code of the Vue website
 ┃ ┗ 📜App.vue            // Main vue component
 ┣ 📜.gitignore
 ┣ 📜package.json         // Node package.json
 ┣ 📜README.md
 ┣ 📜vite.config.js       // Vite configuration
 ┣ 📜index.html           // Main HTML page of the website
 ┣ 📜postcss.config.js    // PostCSS configuration
 ┗ 📜tailwind.config.js   // Tailwind configuration
```

## 💻 Website Setup
The website is built with [Vue 3](https://v3.vuejs.org/) and [Vite](https://vitejs.dev/). It uses [Tailwind CSS](https://tailwindcss.com/) for styling.

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

## 📚 Scripts Setup (Data Gathering)

The scripts are written in Python. They use the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library to parse HTML pages which are gathered from [Liquipedia API](https://liquipedia.net/commons/Liquipedia:API_Usage_Guidelines).

Execute main.py to start collecting data from Liquipedia and generate JSON files.

You can configure the script directly in main.py script "Configuration" section.