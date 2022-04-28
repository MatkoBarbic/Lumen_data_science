import { useState } from "react"
import { useNavigate } from "react-router-dom";
const Home = () => {
    let navigate = useNavigate();
    const [files, setFiles] = useState([])
    const handleUpload = () => {
        // console.log(files)
        // navigate("/guess", {state: {coordinates: [50, 50], image:undefined}})
        if (files.length !== 0) {
            fetch("http://localhost:8000/app/", {
                mode: 'no-cors',
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    files
                }),
            }).then((res) => res.json()).then((res) => navigate("/guess", res))
            // }).then((res) => res.json()).then((res) => navigate("/guess", {state: {coordinates: [50, 50], image: 50}}))
        }
    }
    return (
        <>
            <div className="container-main">
                <h1 className='title-big'>lil GUESSR</h1>
                <div className="container-upload">
                    <h2 className='title-small'>Uploadajte slike ovdje: </h2>
                    {files.length === 0 ?
                    <label className="label-button">Odaberite slike
                        <input type="file" multiple className="input" onChange={(e) => setFiles(e.target.files)} required></input>
                    </label>
                    :
                    <label className="label-button">{files.length} slike odabrano
                        <input type="file" multiple className="input" onChange={(e) => setFiles(e.target.files)} required></input>
                    </label>}

                    <button onClick={handleUpload} className="button">Upload</button>
                </div>
            </div>
        </>
    )
}
export default Home