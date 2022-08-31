pragma solidity ^0.5.5;

import "./ElonMusk.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/CappedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/TimedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/distribution/RefundablePostDeliveryCrowdsale.sol";


// Bootstrap the ElonMuskCrowdsale contract by inheriting the following OpenZeppelin:
// * Crowdsale
// * MintedCrowdsale
contract ElonMuskCrowdsale is Crowdsale, MintedCrowdsale, CappedCrowdsale, TimedCrowdsale, RefundablePostDeliveryCrowdsale {
    
    // Provide parameters for all of the features of crowdsale, such as the `rate`, `wallet` for fundraising, and `token`.
    constructor(
        uint256 rate, // rate in TKNbits
        address payable wallet, // sale beneficiary
        ElonMusk token, // the ElonMusk itself that the BillGatesCrowdsale will work with
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


contract ElonMuskCrowdsaleDeployer {
    // Create an `address public` variable called `elon_token_address`.
    address public elon_token_address;
    // Create an `address public` variable called `elon_crowdsale_address`.
    address public elon_crowdsale_address;

    // Add the constructor.
    constructor(
        string memory name,
        string memory symbol,
        address payable wallet, // this address will receive all Ether raised by the crowdsale
        uint goal
    ) public {
        // Create a new instance of the ElonMusk contract.
        ElonMusk token = new ElonMusk(name, symbol, 0);
        
        // Assign the token contract’s address to the `elon_token_address` variable.
        elon_token_address = address(token);

        // Create a new instance of the `ElonMuskCrowdsale` contract
        ElonMuskCrowdsale elon_crowdsale = new ElonMuskCrowdsale (1, wallet, token, goal, now, now + 24 weeks);
            
        // Aassign the `ElonMuskCrowdsale` contract’s address to the `elon_crowdsale_address` variable.
        elon_crowdsale_address = address(elon_crowdsale);

        // Set the `ElonMuskCrowdsale` contract as a minter
        token.addMinter(elon_crowdsale_address);
        
        // Have the `ElonMuskCrowdsaleDeployer` renounce its minter role.
        token.renounceMinter();
    }
}