import { GetServerSideProps, NextPage } from "next"
import { v4 as uuidv4 } from 'uuid'
import styles from '../../styles/Home.module.css'
import Image from 'next/future/image'

// Define the props interface
interface IProps {
    data: IVideos
};

interface IVideoItem {
    name: string
    source: string
    iconUri: string
    description: string | null
};

interface IVideos {
    count: number
    videos: Array<IVideoItem>
    source: string
};

function handleFilterName(e: any) {
    const name = e.target.value.toLowerCase();
    window.history.pushState({}, '', `?name=${name}`);
    window.location.reload();
}

const Videos: NextPage<IProps> = ({ data }) => {

    return (
        <>
            <h1 style={{ padding: 20 }}>Videos ({data.count})</h1>


            {/* Create text input for filtering data */}
            <div className="input-group mb-3">
                <span className="input-group-text" id="txtSearchByName">
                    Filter: Name
                </span>
                <input
                    type="text"
                    className="form-control"
                    placeholder="Search..."
                    aria-label="Search..."
                    aria-describedby="txtSearchByName"
                    onKeyPress={(e) => e.key === 'Enter' && handleFilterName(e) }
                />
            </div>

            <div className="row justify-content-center">
                {data.videos.map((videoItem: IVideoItem) => (
                    <div key={uuidv4()} className="card" style={{ width: "18rem", border: "1px solid lightgray", padding: "20px", margin: "10px", minHeight: "450px" }}>
                        <Image className="card-img-top" src={videoItem.iconUri} width={200} height={200} alt="Card image cap" />
                        <div className="card-body">
                            <h5 className="card-title">{videoItem.name}</h5>
                            <p className="card-text">{videoItem.description}</p>
                            <a href="#" className="btn btn-primary" style={{ width: "-webkit-fill-available" }}>{videoItem.source}</a>
                        </div>
                    </div>
                ))}
            </div>
        </>
    )
}


export const getServerSideProps: GetServerSideProps = async (context) => {

    // console.log(`[ DEBUG ]: getServerSideProps context: `, context)
    // TODO: logging library
    console.log(`[ DEBUG ] fetching: ${process.env.API_URL}${context.resolvedUrl}`)

    const res = await fetch(`${process.env.API_URL}${context.resolvedUrl}`)
        .catch((err) => {
            console.log(`[ ERROR ] ${err}`)
            return null
        })

    if (res === null) {
        return { props: { data: { count: 0, videos: [] } } }
    }

    const data = await res.json()

    return { props: { data } }
}

export default Videos
