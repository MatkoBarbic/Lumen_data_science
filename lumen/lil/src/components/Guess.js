import { useLocation, useNavigate } from "react-router-dom"

const Guess = () => {
    const location = useLocation()
    const navigate = useNavigate()
    const handleClick = () => {
        navigate("/")
    }
    return(
        <div className="container-coordinates">
            {/* {console.log(location.state)} */}
            <h2 className="title-small">Koordinate:</h2>
            <h2 className="title-small">{location.state.coordinates[0]} N</h2>
            <h2 className="title-small">{location.state.coordinates[1]} E</h2>
            <button className="button" onClick={handleClick}>Nova lokacija</button>
        </div>
    )
}
export default Guess