import { useLocation, useNavigate } from "react-router-dom"

const Guess = () => {
    const location = useLocation()
    const navigate = useNavigate()
    const handleClick = () => {
        navigate("/")
    }
    return(
        <div className="container-coordinates">
            <h2 className="title-small">Coordinates:</h2>
            <h2 className="title-small">{location.state.coordinates[0]} N</h2>
            <h2 className="title-small">{location.state.coordinates[1]} E</h2>
            <button className="button" onClick={handleClick}>New location</button>
        </div>
    )
}
export default Guess