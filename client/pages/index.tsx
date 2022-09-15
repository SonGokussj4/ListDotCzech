import type { NextPage } from 'next'
import Image from 'next/image'
import styles from '../styles/Home.module.css'

const Home: NextPage = () => {
  return (
    <div className={styles.container}>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to ListDotCzech site
        </h1>

        <p className={styles.description}>
          Test application for filtering and caching API response into DB{' '}
        </p>

        <div className={styles.grid}>
          <a href="/videos" className={styles.card} style={{ maxWidth: 900 }}>
            <h2>Start by going to &rarr; /VIDEOS</h2>
            <p></p>
          </a>
        </div>
      </main>

      <footer className={styles.footer}>
        <a
          href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by{' '}
          <span className={styles.logo}>
            <Image src="/vercel.svg" alt="Vercel Logo" width={72} height={16} />
          </span>
        </a>
      </footer>
    </div>
  )
}

export default Home
