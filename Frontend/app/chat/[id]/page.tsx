import Chat from '../../page';
import axios from 'axios';

async function fetchMessages(id: number) {
	'use server';
	let messages = [];
	try {
		const response = await axios.get(
			process.env.NEXT_PUBLIC_API_URL + '/get_messages?pdf_id=' + id,
		);
		messages = response.data.data
	} catch (error) {
		console.error('Error getting messages', error);
	}
	return {
		messages
	};
}

async function ChatWithId({params}:{params:{id: number}}) {
	const {
		messages
	} = await fetchMessages(params.id);

	return <Chat messages={messages} />;
}

export default ChatWithId;
