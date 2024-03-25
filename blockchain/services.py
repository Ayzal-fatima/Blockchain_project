from web3 import Web3

# Initialize Web3 connection
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/2-D9tXfAz8Rr-TCAMLgPU9HQOk6F7a1Q'))  # Replace with your Sepolia RPC URL

# Check if connected
def check_connection():
    if w3.is_connected():
        print("Connected to Sepolia!")
        return True
    else:
        print("Connection failed.")
        return False

CONTRACT_ABI = [
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "userAddress",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "authenticationMethod",
				"type": "string"
			}
		],
		"name": "AttendanceMarked",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "userAddress",
				"type": "address"
			}
		],
		"name": "getAttendance",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "userAddress",
						"type": "address"
					},
					{
						"internalType": "uint256",
						"name": "timestamp",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "authenticationMethod",
						"type": "string"
					}
				],
				"internalType": "struct AttendanceRecord.Record",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "authenticationMethod",
				"type": "string"
			}
		],
		"name": "markAttendance",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "records",
		"outputs": [
			{
				"internalType": "address",
				"name": "userAddress",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "authenticationMethod",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]  
CONTRACT_ADDRESS = '0x28c2a6f63771b632C33bD3852D64b1887e28b5bF' 

# Create an instance of smart contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Sample function to mark attendance
def mark_attendance(student_id, date):
    try:
        tx_hash = contract.functions.markAttendance(student_id, date).transact({'from': '0x4fB1917fDbD2E7E382060Eb0c63C156C5b73A19e'})  
        return tx_hash
    except Exception as e:
        print(f"Error marking attendance: {e}")
        return None

def get_attendance(student_id):
    try:
        attendance_data = contract.functions.getAttendance(student_id).call()
        return attendance_data
    except Exception as e:
        print(f"Error fetching attendance: {e}")
        return None


