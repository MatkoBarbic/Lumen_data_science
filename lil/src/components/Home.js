import { useState } from "react"
import { useNavigate } from "react-router-dom";
const Home = () => {
    let navigate = useNavigate();
    const [files, setFiles] = useState([])
    const handleUpload = () => {
        const formData = new FormData()
        // console.log(files[0])
        if (files.length !== 0) {
            for (var i = 0; i < files.length; i++){
                formData.append(`${i * 90}.jpg`, files[i])
            }
            fetch("http://localhost:8000/app/", {
                method: "POST",
                // headers: {
                //     // "Content-Type": "application/json"
                //     // "Content-Type": "multipart/form-data"
                // },
                body: formData,
            }).then((res) => res.json()).then((res) => navigate("/guess", {state: res}))
            // }).then((res) => res.json()).then((res) => console.log(res))

        }
    }
    return (
        <>
            <div className="container-main">
                <h1 className='title-big'>GEOGUESSR AI</h1>
                <div className="container-upload">
                    <h2 className='title-small'>Upload pictures here: </h2>
                    {files.length === 0 &&
                    <label className="label-button">Choose 
                        <input type="file" multiple className="input" onChange={(e) => setFiles(e.target.files)} required></input>
                    </label>
                    }
                    {files.length === 1 &&
                    <label className="label-button">{files.length} image chosen
                        <input type="file" multiple className="input" onChange={(e) => setFiles(e.target.files)} required></input>
                    </label>
                    }
                    {files.length > 1 &&
                    <label className="label-button">{files.length} images chosen
                        <input type="file" multiple className="input" onChange={(e) => setFiles(e.target.files)} required></input>
                    </label>
                    }

                    <button onClick={handleUpload} className="button">Upload</button>
                </div>
            </div>
        </>
    )
}
export default Home