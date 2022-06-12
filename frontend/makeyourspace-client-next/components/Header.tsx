import React from 'react'
import Link from 'next/link'

function Header() {
  return (
    <header className='flex justify-between p-5 max-w-9xl mx-auto'>
        {/* p-5   padding of 5
            justify-between     will space the children  */}

    <div className='flex items-center space-x-5'>
        <Link href="/">
            <h1 className='cursor-pointer font-extrabold text-3xl italic'>MakeYourSpace</h1>
        </Link>

        <div className='hidden md:inline-flex items-center space-x-5'>
            <h3>MyPosts</h3>
            <h3 className='text-white bg-blue-800 px-4 py-1 rounded-full'>Create</h3>
            {/* px-4   padding on y-axis of 4
                py-1   padding on x-axis of 1 */}
        </div>

    </div>

    <div className='flex items-center space-x-5'>

        <h3>Sign In</h3>
        <h3>Stories</h3>
        <h3>Settings</h3>

    </div>
      
    </header>
  )
}

export default Header
