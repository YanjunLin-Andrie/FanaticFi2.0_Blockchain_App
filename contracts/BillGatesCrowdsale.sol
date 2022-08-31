pragma solidity ^0.5.5;

import "./BillGates.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/CappedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/TimedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/distribution/RefundablePostDeliveryCrowdsale.sol";


// Bootstrap the BillGatesCrowdsale contract by inheriting the following OpenZeppelin:
// * Crowdsale
// * MintedCrowdsale
contract BillGatesCrowdsale is Crowdsale, MintedCrowdsale, CappedCrowdsale, TimedCrowdsale, RefundablePostDeliveryCrowdsale {
    
    // Provide parameters for all of the features of crowdsale, such as the `rate`, `wallet` for fundraising, and `token`.
    constructor(
        uint256 rate, // rate in TKNbits
        address payable wallet, // sale beneficiary
        BillGates token, // the BillGates itself that the BillGatesCrowdsale will work with
        uint goal, // the crowdsale goal
        uint open, // the crowdsale opening time
        uint close // the crowdsale closing time
    ) public
        Crowdsale(rate, wallet, token)
        CappedCrowdsale(goal)
        TimedCrowdsale(open, close)
        RefundableCrowdsale(goal)
    {
        // constructor can stay empty
    }
}


contract BillGatesCrowdsaleDeployer {
    // Create an `address public` variable called `bill_token_address`.
    address public bill_token_address;
    // Create an `address public` variable called `bill_crowdsale_address`.
    address public bill_crowdsale_address;

    // Add the constructor.
    constructor(
        string memory name,
        string memory symbol,
        address payable wallet, // this address will receive all Ether raised by the crowdsale
        uint goal
    ) public {
        // Create a new instance of the BillGates contract.
        BillGates token = new BillGates(name, symbol, 0);
        
        // Assign the token contract’s address to the `bill_token_address` variable.
        bill_token_address = address(token);

        // Create a new instance of the `BillGatesCrowdsale` contract
        BillGatesCrowdsale bill_crowdsale = new BillGatesCrowdsale (1, wallet, token, goal, now, now + 24 weeks);
            
        // Aassign the `BillGatesCrowdsale` contract’s address to the `bill_crowdsale_address` variable.
        bill_crowdsale_address = address(bill_crowdsale);

        // Set the `BillGatesCrowdsale` contract as a minter
        token.addMinter(bill_crowdsale_address);
        
        // Have the `BillGatesCrowdsaleDeployer` renounce its minter role.
        token.renounceMinter();
    }
}