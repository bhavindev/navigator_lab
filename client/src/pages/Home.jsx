import React, { useEffect, useState } from 'react'
import useAuth from '../hooks/useAuth'
import useUser from '../hooks/useUser';
import Web3 from 'web3';

export default function Home() {
    const { user } = useAuth();
    const getUser = useUser()
    const ethereum_wallet_address = user?.ethereum_wallet_address
    const ethereum_wallet_balance = user?.ethereum_wallet_balance

    useEffect(() => {
        getUser()
    }, [])

    return (
        <div className='container mt-3'>
            <h2>
                <div className='row'>
                    <div className="mb-12">
                        {user?.email !== undefined ? (
                            <>
                            <h1>List user Ethereum balance</h1>
                            <table border={1} style={{"width":"100%"}}>
                                <thead>
                                    <tr>
                                        <th>Wallet Address</th>
                                        <th>Balance</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>{!ethereum_wallet_address?'Wallet Address not Available':ethereum_wallet_address}</td>
                                        <td>{ethereum_wallet_balance}</td>
                                    </tr>
                                </tbody>
                            </table>
                            </>
                        ) : 'Please login first'}
                        
                    </div>
                </div>
            </h2>
        </div>
    )
}
