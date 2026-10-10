import http from 'k6/http';
import {check, sleep} from 'k6';

export const options = {
    vus: 20,
    duration: '60s',
    thresholds: {
        http_req_failed: ['rate<=0.1'],
        checks: ['rate>=0.99']
    }
};


const shortCodes = [
  'aB7kP2',
  'aY8tF6',
  'bM8yF4',
  'cJ6qT4',
  'dK1pW9',
  'dV5bN2',
  'eW6rQ2',
  'fA2kY9',
  'gN5cV3',
  'hK9dA1',
  'iM5zR4',
  'jQ8pD4',
  'kF9pR1',
  'lH3qP8',
  'mN4xQ9',
  'nP3zW6',
  'oC7vN2',
  'pL1wX8',
  'qR7mK5',
  'rT8vL3',
  'rX4bJ7',
  'sT4jL7',
  'tB9xM5',
  'tlCt5t',
  'tlCt8t',
  'uX1mB8',
  'vR6nC1',
  'wY2cD6',
  'xC2tH9',
  'yD4wK7',
];

export default function(){
    const index = Math.floor(Math.random()*shortCodes.length);
    const code = shortCodes[index];
    const response = http.get(`http://localhost:80/${code}`,
        {
            redirects: 0,
            timeout: '1s'
        }
    );

    check(response, {
        'redirect 307 or not': (r)=> r.status === 307
    });

    sleep(0.1);
}