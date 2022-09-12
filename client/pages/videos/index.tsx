import Head from "next/head"
import { GetServerSideProps, NextPage } from "next"
import { v4 as uuidv4 } from 'uuid';

// Define the props interface
interface IProps {
    data: IVideos
};

interface IVideoItem {
    name: string
    source: string
};

interface IVideos {
    count: number
    videos: Array<IVideoItem>
};


const Videos: NextPage<IProps> = ({ data }) => {

    return (
        <>
            <Head>
                <title>Videos</title>
            </Head>

            <h1>Videos</h1>

            <div>
                {data.videos.map((video: IVideoItem) => (
                    <div key={uuidv4()}>
                        <h2>{video.name}</h2>
                        <p>Source: {video.source}</p>
                    </div>
                ))}
            </div>
        </>
    )
}


export const getServerSideProps: GetServerSideProps = async () => {

    // TODO: logging library
    console.log(`[ DEBUG ] fetching: ${process.env.API_URL}/videos`)

    const res = await fetch(`${process.env.API_URL}/videos`)
    const data = await res.json()

    return { props: { data } }
}

export default Videos
