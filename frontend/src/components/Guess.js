import { useLocation, useNavigate } from "react-router-dom"
import result from '../images/result_visualization.jpg'
const Guess = () => {
    const location = useLocation()
    const navigate = useNavigate()
    const handleClick = () => {
        navigate("/")
    }
    return(
        <>
            {console.log(location.state)}
            <img src={result} className="background"></img>
            <div className="container-coordinates">
                <h2 className="title-small">Coordinates:</h2>
                <h2 className="title-small">{(location.state.x * (19.45 - 13.5) + 13.5).toFixed(7)} E</h2>
                <h2 className="title-small">{(location.state.y * (46.55 - 42.4) + 42.4).toFixed(7)} N</h2>
                <button className="button" onClick={handleClick}>New location</button>
            </div>
        </>
    )
}
export default Guess