import Button from 'react-bootstrap/Button';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import "./DisableButton.css";

function DisableButton() {
  return (
    <div className="btm_left">
      <OverlayTrigger overlay={<Tooltip id="tooltip-disabled">Log as Admin to access</Tooltip>}>
        <span className="d-inline-block">
          <Button disabled style={{ pointerEvents: 'none' }}>
            Admin mod
          </Button>
        </span>
      </OverlayTrigger>
    </div>
  );
}

export default DisableButton;
