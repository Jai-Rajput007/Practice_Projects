'use client';
import {useState, useEffect } from 'react';
import {Input} from '@/components/ui/input';
import {Button} from '@/components/ui/button';
import { Card,CardContent,CardHeader,CardTitle } from '@/components/ui/card';
import { Alert,AlertDescription,AlertTitle } from '@/components/ui/alert';
import Slider from 'react-slick';

interface ScrapedItem{
  id:number;
  title:string;
  content:string;
  created_at:string;
}

export default function Home(){
  const [url,setUrl] = useState('');
  const [results,setResults] = useState<ScrapedItem[]>([]);
  const [loading,setLoading] = useState(false);
  const [error,setError] = useState<string|null>(null);


const sliderSettings = {
  dots:true,
  infinite: results.length>1,
  speed :500,
  slidesToShow: 1,
  slidesToScroll: 1,
  arrows:true,
  autoplay:false,
};

const fetchResults = async() =>{
  try{
    const response = await fetch('/api/results');
    if(!response.ok) throw new Error('Failed to fetch results');
    const data:ScrapedItem[] = await response.json();
    setResults(data);
  } catch(err:unknown){
    const errorMessage = err instanceof Error ? err.message :'An unknown error occured';
     setError(errorMessage);
  }
};


const handleSubmit = async(e:React.FormEvent) => {
 e.preventDefault();
if(!url.match(/^https?:\/\/.+/)){
  setError('Please enter a valid URL starting with http:// or https://');
  return;
}
setLoading(true);
setError(null);
try{
  const response = await fetch ('/api/scrape',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({url}),
  });
  if(!response.ok) throw new Error('Scraping failed');
  await fetchResults();
}catch(err:unknown){
  const errorMessage = err instanceof Error ? err.message:'An unknown error occured';
  setError(errorMessage);
} finally{
  setLoading(false);
}
};

const handleClear = async() => {
  setLoading(true);
  setError(null);
  try{
    const response = await fetch('/api/clear',{method:"Post"});
    if(!response.ok) throw new Error('Failed to clear data');
    await fetchResults();
  }catch(err:unknown){
    const errorMessage= err instanceof  Error? err.message:'An unknown error occured';
    setError(errorMessage);
  }finally{
    setLoading(false);
  }
};

useEffect(()=>{
  fetchResults();
},[]);

return (
  <div className='container mx=auto p-4'>
    <Card className='max-w-4xl mx-auto'>
      <CardHeader>
        <CardTitle>Web Scraper</CardTitle>
      </CardHeader>
      <CardContent>
      <form onSubmit={handleSubmit} className='flex gap-2 mb-4'>
        <Input 
        type="text"
        value ={url}
        onChange = {(e) => setUrl(e.target.value)}
        placeholder='Enter URL (e.g., https://example.com/)'
        className='flex-1'
        disabled = {loading} />
       <Button type = "submit" disabled = {loading}>
        {loading ? 'Scraping...':"Scrape"}
       </Button>
       <Button 
       variant = "outline"
       onClick = {handleClear}
       disabled ={loading}>
        Clear Data
       </Button>
      </form>
      {error && (
        <Alert variant ="destructive" className="mb-4">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
      <h2 className='text-lg font-semibold mb-2'>Scraped Results </h2>
      {results.length ===0?(
        <p className='text-gray-500'>No data available. Try scraping a URL!</p>
      ):(
        <Slider{...sliderSettings} className = "mb-4">
        {results.map((item) => (
        <div key={item.id} className="p-4">
        <Card>
        <CardContent className='pt-4'>
        <h3 className='font-semibold'>{item.title}</h3>
        <p className='text-gray-600'>Content:{item.content}</p>
        <p className='text-sm text-gray-500'>
        Created At:{new Date(item.created_at).toLocaleString()}
        </p>
        </CardContent>
        </Card>
        </div>
        ))}
        </Slider>
      )}
      </CardContent>
    </Card>
  </div>
);
}