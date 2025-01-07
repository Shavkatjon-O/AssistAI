import Image from "next/image";

const Page = () => {
  return (
    <div className="h-screen flex justify-center items-center">
      <div className="flex flex-col justify-center items-center">
        <Image
          src="/assistai.png"
          alt="AssistAI Logo"
          width={256}
          height={256}
          className="animate-bounce"
        />
        <div>
          Coming Soon ...
        </div>
      </div>
    </div>
  );
};
export default Page;