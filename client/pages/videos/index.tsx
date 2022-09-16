import { GetServerSideProps, NextPage } from "next"
import Select from 'react-select';
import { v4 as uuidv4 } from 'uuid'
import styles from '../../styles/Home.module.css'
import Image from 'next/future/image'
import Badge from 'react-bootstrap/Badge'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'



interface IProps {
    data: IVideos
    filterItems: IFilterItems
};

interface IFilterItems {
    name: Array<string>
    disabled: boolean
    features: Array<string>
}
interface IVideoItem {
    name: string
    source: string
    iconUri: string
    description: string | null
    features: Array<string>
};

interface IVideos {
    count: number
    videos: Array<IVideoItem>
    source: string
};

const Videos: NextPage<IProps> = ({ data, filterItems }) => {

    const router = useRouter()

    const [videos, setVideos] = useState(data.videos)
    const [sortBy, setSortBy] = useState({ label: "Name", value: "name" })
    const [filterName, setFilterName] = useState(router.query )

    function handleFilterNameSubmit(e: any) {
        const name = e.target.value.toLowerCase();
        window.history.pushState({}, '', `?name=${name}`);
        window.location.reload();
    }

    function handleFilterName(e: any) {
        setFilterName({ name: e.target.value.toLowerCase() })
    }

    const handleFilterFeatures = (e: any) => {
        console.log(e)
    }

    function handleSortBy(e: any) {
        setSortBy(e)

        if (e.value === "name") {
            videos.sort((a, b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0))
        } else if (e.value === "source") {
            videos.sort((a, b) => (a.source > b.source) ? 1 : ((b.source > a.source) ? -1 : 0))
        }

    }

    return (
        <>
            <h1 style={{ padding: 20 }}>Videos ({data.count}) (Source: {data.source})</h1>

            <div className="d-flex justify-content-center align-items-center">
                <button
                    type="button"
                    className="btn btn-primary"
                    data-bs-toggle="modal"
                    data-bs-target="#exampleModal"
                >
                    Launch demo modal
                </button>

                <div
                    className="modal fade"
                    id="exampleModal"
                    tabIndex={-1}
                    aria-labelledby="exampleModalLabel"
                    aria-hidden="true"
                >
                    <div className="modal-dialog">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title" id="exampleModalLabel">
                                    Modal title
                                </h5>
                                <button
                                    type="button"
                                    className="btn-close"
                                    data-bs-dismiss="modal"
                                    aria-label="Close"
                                ></button>
                            </div>
                            <div className="modal-body">
                                And some content here
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Create text input for filtering data */}
            <div className="input-group mb-3" style={{ width: 500, padding: 10 }}>
                <span className="input-group-text" id="txtSearchByName" style={{ width: 140 }}>
                    <Badge pill bg="secondary" style={{ marginRight: 5 }}>BE</Badge> Filter: Name
                </span>
                <input
                    value={filterName.name}
                    type="text"
                    className="form-control"
                    placeholder="Search..."
                    aria-label="Search..."
                    aria-describedby="txtSearchByName"
                    onChange={handleFilterName}
                    onKeyPress={(e) => e.key === 'Enter' && handleFilterNameSubmit(e)}
                />
            </div>
            <div className="mb-3" style={{ width: 500, padding: 10 }}>
                <span className="input-group-text" id="txtSortBy" style={{ width: 140 }}>
                    Features (multi) . . Not working for now
                </span>
                <Select
                    // value={filterItems.selectedFeatures}
                    isMulti
                    onChange={handleFilterFeatures}
                    options={filterItems.features.map((opt: string) => ({ label: opt, value: opt }))}
                />
            </div>
            <div className="mb-3" style={{ width: 500, padding: 10 }}>
                <span className="input-group-text" id="txtSortBy" style={{ width: 140 }}>
                    <Badge pill bg="secondary" style={{ marginRight: 5 }}>FE</Badge> Sort by:
                </span>
                <Select
                    value={sortBy}
                    onChange={handleSortBy}
                    options={[
                        { label: "Name", value: "name" },
                        { label: "Source", value: "source" }
                    ]}
                />
            </div>

            <div className="row justify-content-center">
                {videos.map((videoItem: IVideoItem) => (
                    <div key={uuidv4()} className="card" style={{ width: "18rem", border: "1px solid lightgray", padding: "20px", margin: "10px", minHeight: "450px" }}>
                        <Image className="card-img-top" src={videoItem.iconUri} width={200} height={200} alt="Card image cap" />

                        <div className="card-body">
                            <h5 className="card-title">{videoItem.name}</h5>
                            <p className="card-text">Source: {videoItem.source}</p>
                            <p className="card-text">{videoItem.description}</p>
                            {videoItem.features.map((feature: string) => (
                                <Badge pill key={uuidv4()} bg="primary" style={{ margin: "5px" }}>{feature}</Badge>
                            ))}
                        </div>

                    </div>
                ))}
            </div>
        </>
    )
}


export const getServerSideProps: GetServerSideProps = async (context) => {

    const filterItemsRes = await fetch(`${process.env.API_URL}/getFilterItems?name=${context.query?.name ? context.query?.name : ''}`)
        .catch((err) => {
            console.log(`[ ERROR ] ${err}`)
            return null
        })
    const filterItems = await filterItemsRes?.json()

    const res = await fetch(`${process.env.API_URL}${context.resolvedUrl}`)
        .catch((err) => {
            console.log(`[ ERROR ] ${err}`)
            return null
        })

    if (res === null) {
        return { props: { data: { count: 0, videos: [] } } }
    }

    const data = await res.json()

    return {
        props: {
            data,
            filterItems
        }
    }
}

export default Videos
